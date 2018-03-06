import os


# Loads data for both books and movies, returning a dictionary with two keys, 'books' and 'movies', one for
# each subset of the collection.
def load_collections():
    # Load the two collections.
    book_collection, max_book_id = load_collection("books.csv")
    movie_collection, max_movie_id = load_collection("movies.csv")
    # Check for error.
    if (book_collection is None) or (movie_collection is None):
        return None, None
    # Return the composite dictionary.
    return {"books": book_collection, "movies": movie_collection}, max(max_book_id, max_movie_id)


# Loads a single collection and returns the data as a list.  Upon error, None is returned.
def load_collection(file_name):
    max_id = -1
    try:
        # Create an empty collection.
        collection = []
        # Open the file and read the field names
        collection_file = open(file_name, "r")
        field_names = collection_file.readline().rstrip().split(",")

        # Read the remaining lines, splitting on commas, and creating dictionaries (one for each item)
        for item in collection_file:
            field_values = item.rstrip().split(",")
            collection_item = {}
            for index in range(len(field_values)):
                if (field_names[index] == "Available") or (field_names[index] == "Copies") or (field_names[index] == "ID"):
                    collection_item[field_names[index]] = int(field_values[index])
                else:
                    collection_item[field_names[index]] = field_values[index]
            # Add the full item to the collection.
            collection.append(collection_item)
            # Update the max ID value
            max_id = max(max_id, collection_item["ID"])

        # Close the file now that we are done reading all of the lines.
        collection_file.close()

    # Catch IO Errors, with the File Not Found error the primary possible problem to detect.
    except FileNotFoundError:
        print("File not found when attempting to read", file_name)
        return None
    except IOError:
        print("Error in data file when reading", file_name)
        collection_file.close()
        return None

    # Return the collection.
    return collection, max_id


# Display the menu of commands and get user's selection.  Returns a string with the user's requested command.
# No validation is performed.
def prompt_user_with_menu():
    print("\n\n********** Welcome to the Collection Manager. **********")
    print("COMMAND    FUNCTION")
    print("  ci         Check in an item")
    print("  co         Check out an item")
    print("  ab         Add a new book")
    print("  am         Add a new movie")
    print("  db         Display books")
    print("  dm         Display movies")
    print("  qb         Query for books")
    print("  qm         Query for movies")
    print("  s          Save changes")
    print("  x          Exit")
    return input("Please enter a command to proceed: ")


def check_id():
    not_valid = True
    while not_valid:
        try:
            id_value = int(input('Enter the ID for the item you wish to check in or out: '))
            not_valid = False
        except ValueError:
            print('ID number must be integer! ')
    return id_value


def check_copies():
    not_valid = True
    while not_valid:
        try:
            copy_value = int(input('Copies: '))
            not_valid = False
        except ValueError:
            print('Copies number must be integer! ')
    return copy_value


def show_record(record):
    for key in record:
        if key != 'ID':
            print(key, ':', record[key])


def check_in(library_collections):
    id_number = check_id()
    all_collections = library_collections['books'] + library_collections['movies']
    found = False
    for item in all_collections:
        if item['ID'] == id_number:
            found = True
            # check whether the item is checked out
            if item['Available'] < item['Copies']:
                item['Available'] += 1
                print('Your check in has succeed.')
                print()
                print('ID:', item['ID'])
                show_record(item)
            else:
                print('All copies are already available, so this item can not be checked in')
    if not found:
        print('The ID can not be found, please check again.')


def check_out(library_collections):
    id_number = check_id()
    all_collections = library_collections['books'] + library_collections['movies']
    found = False
    for item in all_collections:
        if item['ID'] == id_number:
            found = True
            # check whether the item is available
            if item['Available'] != 0:
                item['Available'] -= 1
                print('Your check out has succeeded.')
                print('ID:',item['ID'])
                show_record(item)
            else:
                print('No copies of the item are available for check out.')
    if not found:
        print('The ID can not be found, please check again.')


def check_existing_and_update(library_collection, max_existing_id, record):
    for item in library_collection:
        existing = True
        record['Available'] = item['Available']
        record['ID'] = item['ID']
        for key in item:
            if key != 'Copies':
                if item[key] != record[key]:
                    existing = False
        if existing:
            item['Copies'] += record['Copies']
            item['Available'] += record['Copies']
            print('The item is existing. Add more', record['Copies'], 'to the library collection')
            break
    if not existing:
        max_existing_id += 1
        record['Available'] = record['Copies']
        record['ID'] = max_existing_id
        library_collection.append(record)
        print('New item is added to the library collection')


def add_book(book_collections, max_existing_id):
    print('Please enter the following attributes for the new book.')
    book_item = {}
    book_item['Title'] = input('Title:')
    book_item['Author'] = input('Author:')
    book_item['Publisher'] = input('Publisher:')
    book_item['Pages'] = input('Pages:')
    book_item['Year'] = input('Year:')
    book_item['Copies'] = check_copies()
    print('You have entered the following data:')
    show_record(book_item)
    confirm_add = input("Press enter to add this item to the collection.  Enter 'x' to cancel.")
    while confirm_add != '' and confirm_add != 'x':
        confirm_add = input("Press enter to add this item to the collection.  Enter 'x' to cancel.")
    if confirm_add == '':
        check_existing_and_update(book_collections, max_existing_id, book_item)
        print('Your add has succeed. ')
    elif confirm_add == 'x':
        print('Your add has cancelled. ')
    return max_existing_id


def add_movie(movie_collections, max_existing_id):
    print('Please enter the following attributes for the new movie.')
    movie_item = {}
    movie_item['Title'] = input('Title:')
    movie_item['Director'] = input('Director:')
    movie_item['Length'] = input('Length:')
    movie_item['Genre'] = input('Genre:')
    movie_item['Year'] = input('Year:')
    movie_item['Copies'] = check_copies()
    print('You have entered the following data:')
    show_record(movie_item)
    confirm_add = input("Press enter to add this item to the collection.  Enter 'x' to cancel.")
    while confirm_add != '' and confirm_add != 'x':
        confirm_add = input("Press enter to add this item to the collection.  Enter 'x' to cancel.")
    if confirm_add == '':
        check_existing_and_update(movie_collections, max_existing_id, movie_item)
        print('Your add has succeed. ')
    elif confirm_add == 'x':
        print('Your add has cancelled. ')
    return max_existing_id


def display_collection(library_collections):
    count_start = 0
    count_end = 0
    for item in library_collections:
        print('ID:', item['ID'])
        show_record(item)
        print()
        count_end += 1
        if (count_end - count_start) == 10:
            count_start = count_end
            show_more = input("Press enter to show more items, or type 'm' to return to the menu.")
            while show_more != '' and show_more != 'm':
                show_more = input("Press enter to show more items, or type 'm' to return to the menu.")
            if show_more == '':
                continue
            elif show_more == 'm':
                break


def query_collection(library_collections):
    search = input("Enter a query string to use for the search:")
    while search == '':
        search = input("Enter a query string to use for the search:")
    search = search.lower()
    found = False
    for item in library_collections:
        flag = False
        for key in item:
            if key == 'Title' or key == 'Author' or key == 'Publisher' or key == 'Director' or key == 'Genre':
                if search in item[key].lower():
                    found = True
                    flag = True
        if flag:
            print('ID:', item['ID'])
            show_record(item)
            print()
    if not found:
        print("not found .  Please try again.")


def save_change(library_collections):
    temp_book = open('temp_book.csv', 'a')
    temp_movie = open('temp_movie.csv', 'a')

    for item in library_collections['books']:
        count = 0
        for k in item.keys():
            count += 1
            if count < len(item):
                temp_book.write(str(k) + ',')
            elif count == len(item):
                temp_book.write(str(k) + '\n')
        break

    for item in library_collections['books']:
        count = 0
        for v in item.values():
            count += 1
            if count < len(item):
                temp_book.write(str(v) + ',')
            elif count == len(item):
                temp_book.write(str(v)+'\n')

    for item in library_collections['movies']:
        count = 0
        for k in item.keys():
            count += 1
            if count < len(item):
                temp_movie.write(str(k) + ',')
            elif count == len(item):
                temp_movie.write(str(k)+'\n')
        break

    for item in library_collections['movies']:
        count = 0
        for v in item.values():
            count += 1
            if count < len(item):
                temp_movie.write(str(v) + ',')
            elif count == len(item):
                temp_movie.write(str(v)+'\n')
    temp_book.close()
    temp_movie.close()
    os.remove('books.csv')
    os.rename('temp_book.csv', 'books.csv')
    os.remove('movies.csv')
    os.rename('temp_movie.csv', 'movies.csv')
    print('Your save has succeed. ')

# This is the main program function.  This function should (1) Load the data and (2) Manage the main program loop that
# lets the user perform the various operations (ci, co, qb, etc.)
def main():
    # Load the collections, and check for an error.
    library_collections, max_existing_id = load_collections()
    if library_collections is None:
        print("The collections could not be loaded. Exiting.")
        return
    print("The collections have loaded successfully.")

    # Display the menu and get the operation code entered by the user.  We perform this continuously until the
    # user enters "x" to exit the program.  Calls the appropriate function that corresponds to the requested operation.
    operation = prompt_user_with_menu()
    while operation != "x":
        if (operation == "ci"):
            check_in(library_collections)
        elif (operation == "co"):
            check_out(library_collections)
        elif (operation == "ab"):
            max_existing_id = add_book(library_collections['books'], max_existing_id)
        elif (operation == "am"):
            max_existing_id = add_movie(library_collections['movies'], max_existing_id)
        elif (operation == "db"):
            display_collection(library_collections["books"])
        elif (operation == "dm"):
            display_collection(library_collections["movies"])
        elif (operation == "qb"):
            query_collection(library_collections["books"])
        elif (operation == "qm"):
            query_collection(library_collections["movies"])
        elif (operation == 's'):
            save_change(library_collections)
        else:
            print("Unknown command.  Please try again.")

        operation = prompt_user_with_menu()


main()

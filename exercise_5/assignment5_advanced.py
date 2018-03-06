# Present the user with a menu of options
# Enter the patient-study filename
# Add a patient record
# Delete a patient record
# Count the number of patients in a specific study
# Display the patients in a specific study

# Detect records that cause errors and allow the user to correct them via your program.
# Note that detecting extra blank lines between patient records can be corrected automatically without requiring user intervention.
# Missing study or age data or incorrectly formatted age records require user input.

# Generate a report that displays all unique study numbers with a count of the patients enrolled in each study
# Generate a report that displays all patients who are in more than one study.
# Search for patient records by patient name and display results to the user
# Search for patient records by age for a specific study number and display results to the user
# Quit

# in this program, all the functions are built on messed up file
# there is a function to detect and correct function
# unless user use that function ,the messed up file will not be corrected

import os


# open the file can check its validity
def open_and_validate_file():
    is_filename_valid = False
    while not is_filename_valid:
        try:
            filename = input('Please enter the filename(including its extension name):')
            data_file = open(filename, 'r')
            print("The file has been found")
            data_file.close()
            is_filename_valid = True
        except FileNotFoundError:
            print("You must enter a valid filename!")
    return filename


# count patient records, this function will no longer be used.
def count_records(filename):
    count = 0
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    while patient_name != '':
        if patient_name != '\n':
            patient_age = data_file.readline()
            study_num = data_file.readline()
            count += 1
        patient_name = data_file.readline()
    data_file.close()
    return count


# add name and check its validity
def check_and_add_age():
    is_patient_age_valid = False
    while not is_patient_age_valid:
        try:
            # make sure the age is between 21 dao 70 included
            patient_age = int(input("Please enter the patient age: "))
            while patient_age < 21 or patient_age > 70:
                patient_age = int(input("Please enter the age between 21 and 70 included: "))
            is_patient_age_valid = True
        except ValueError:
            # if the age is not int, print message
            print("You must enter a valid age")
    return patient_age


# display one record check the data at the same time, print according corresponding message
def display_certain_record(data_file, patient_name, patient_age, patient_study):
    # print patient name
    print(patient_name)
    # if patient age is empty
    if patient_age == '\n':
        print(patient_name, 'do not have data for age!')
    else:
        try:
            patient_age = patient_age.rstrip('\n')
            age = int(patient_age)
            # if patient age is not between 21 and 70
            if (age >= 21) and (age <= 70):
                print(patient_age)
            else:
                print(patient_age, 'is invalid number for patient age!')
        except ValueError:
            # if patient age is not int
            print(patient_age, 'is invalid number for patient age!')
    # if study number is empty
    if patient_study == '\n':
        print(patient_name, 'do not have data for study number!')
    else:
        patient_study = patient_study.rstrip('\n')
        print(patient_study)


# any other exception needed in this session?
# add a patient record to the file and print method
def add_a_patient_record(filename):
    try:
        data_file = open(filename, 'a')
        new_patient_name = input("Please enter the patient name you want to add: ")
        new_patient_age = check_and_add_age()
        new_study_num = input("Please enter the patient study number you want to add: ")
        data_file.write(new_patient_name + '\n')
        # pay attention only str can be write into file
        data_file.write(str(new_patient_age) + '\n')
        data_file.write(new_study_num + '\n')
        print("The patient record is added to the file", filename, "sucessfully! ")
    except IOError:
        print("The patient record is no added to the file! ")
    finally:
        data_file.close()


# need some work!
# after the function, the empty line is deleted as well, is it ok?
# this function is built on messed up file, because only patient name parameter can not be empty
# so delete by patient name
# in real situation, I can correct the file then match three parameter to find the record, that will be much easier
def delete_a_patient_record(filename):
    found = False
    delete = input("Please enter the name of patient you want to delete record: ")
    data_file = open(filename, 'r')
    temp_file = open("temp.txt", 'w')
    patient_name = data_file.readline()
    while patient_name != '':
        # pay attention if it is not drop '\n', the next statement can never equal
        if patient_name != '\n':
            patient_name = patient_name.rstrip('\n')
            if patient_name != delete:
                patient_age = data_file.readline()
                study_num = data_file.readline()
                temp_file.write(patient_name + '\n')
                temp_file.write(patient_age)
                temp_file.write(study_num)
            else:
                found = True
                age_delete = data_file.readline()
                study_num_delete = data_file.readline()
        patient_name = data_file.readline()
    data_file.close()
    temp_file.close()
    os.remove(filename)
    os.rename('temp.txt', filename)
    if found:
        print("The record is deleted successfully! ")
    else:
        print("The item is not found in the file! ")


def count_num_of_patient_in_specific_study(filename, study_num):
    found = False
    count = 0
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    while patient_name != '':
        patient_age = data_file.readline()
        patient_study = data_file.readline()
        if patient_study != '\n':
            if patient_study.rstrip('\n') == study_num:
                count += 1
                found = True
        patient_name = data_file.readline()
    if found:
        print('study number: ', study_num, 'has', count, 'patients enrolled')
    else:
        print("There is no record of study number", study_num)
    data_file.close()


# display all the records ! need some work
def display_patients_in_specific_study(filename, study_num):
    data_file = open(filename, 'r')
    found = False
    patient_name = data_file.readline()
    while patient_name != '':
        if patient_name != '\n':
            patient_age = data_file.readline()
            patient_study = data_file.readline()
            patient_name = patient_name.rstrip('\n')
            if patient_study.rstrip('\n') == study_num:
                display_certain_record(data_file, patient_name, patient_age, patient_study)
                found = True
        patient_name = data_file.readline()
        if not found:
            print('There is no record of patient in study number', study_num)
    data_file.close()


# detect and correct the messed up file
def detect_and_correct_records(filename):
    data_file = open(filename, 'r')
    temp_file = open('temp.txt', 'w')
    patient_name = data_file.readline()
    while patient_name != '':
        if patient_name != '\n':
            temp_file.write(patient_name)
            patient_age = data_file.readline()
            if patient_age == '\n':
                print(patient_name.strip('\n'), 'do not have data for age!')
                patient_age = str(check_and_add_age())
                temp_file.write(patient_age + '\n')
            else:
                try:
                    patient_age = patient_age.rstrip('\n')
                    age = int(patient_age)
                    if (age >= 21) and (age <= 70):
                        temp_file.write(patient_age + '\n')
                    else:
                        print(patient_age, 'is invalid number of patient age of', patient_name.rstrip('\n'), '!')
                        patient_age = str(check_and_add_age())
                        temp_file.write(patient_age + '\n')
                except ValueError:
                    print(patient_age, 'is invalid number of patient age of', patient_name.rstrip('\n'), '!')
                    patient_age = str(check_and_add_age())
                    temp_file.write(patient_age + '\n')
            study_num = data_file.readline()
            if study_num == '\n':
                print(patient_name.strip('\n'), 'do not have data for study number!')
                study_num = input('Please enter the patient study number: ')
                temp_file.write(study_num + '\n')
            else:
                temp_file.write(study_num)
        patient_name = data_file.readline()
    data_file.close()
    temp_file.close()
    os.remove(filename)
    os.rename('temp.txt', filename)
    print("Records are all corrected!")


# print how many patients each unique study number
'''
solution 1 (a little complicated)
def report_unique_study_numbers(filename):
    count = count_records(filename)
    is_unique_study = True
    # use record count to form lists
    study = [0] * count
    count_each_study = [0] * count
    index = 0
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    while patient_name != '':
        if patient_name != '\n':
            patient_age = data_file.readline()
            patient_study = data_file.readline()
            if patient_study != '\n':
                study[index] = patient_study.rstrip('\n')
                # read file from the very beginning
                read_data_file_again = open(filename, 'r')
                patient_name_record = read_data_file_again.readline()
                # check the whether study is different
                for i in range(len(study)):
                    if study[i] == study[index] and i != index:
                        is_unique_study = False
                # when study number is different, then count patient numbers in this study
                if is_unique_study:
                    while patient_name_record != '':
                        if patient_name_record != '\n':
                            patient_age_record = read_data_file_again.readline()
                            patient_study_record = read_data_file_again.readline()
                            if patient_study_record.rstrip('\n') == study[index]:
                                count_each_study[index] += 1
                        patient_name_record = read_data_file_again.readline()
                    print(study[index], 'has', count_each_study[index], 'patients enrolled')

        patient_name = data_file.readline()
        read_data_file_again.close()
        index += 1
    data_file.close()
'''


# solution 2: (use 'in' method)
def report_unique_study_numbers(filename):
    unique_study = []
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    # append all the unique study number to the list
    while patient_name != '':
        patient_age = data_file.readline()
        patient_study = data_file.readline()
        if patient_study != '\n':
            study = patient_study.rstrip('\n')
            if study not in unique_study:
                unique_study.append(study)
        patient_name = data_file.readline()
    data_file.close()
    # count the number of specific study number
    for item in unique_study:
        count_num_of_patient_in_specific_study(filename, item)

'''
solution 1: a little complicated
# print patients in more than one study.
def report_patients_in_more_than_one_study(filename):
    count = count_records(filename)
    is_same_patient = False

    patient = [0] * count
    count_each_patient = [0] * count
    index = 0
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    while patient_name != '':
        if patient_name != '\n':
            patient_age = data_file.readline()
            patient_study = data_file.readline()
            if patient_study != '\n':
                patient[index] = patient_name.rstrip('\n')
                read_data_file_again = open(filename, 'r')
                patient_name_record = read_data_file_again.readline()

                for i in range(len(patient)):
                    if patient[i] == patient[index] and i != index:
                        is_same_patient = True

                if not is_same_patient:
                    while patient_name_record != '':
                        if patient_name_record != '\n':
                            patient_age_record = read_data_file_again.readline()
                            patient_study_record = read_data_file_again.readline()
                            if patient_name_record.rstrip('\n') == patient[index]:
                                count_each_patient[index] += 1
                        patient_name_record = read_data_file_again.readline()
                    if count_each_patient[index] > 1:
                        print(patient[index], "is in", count_each_patient[index], 'studies')
        patient_name = data_file.readline()
        read_data_file_again.close()
        index += 1
    data_file.close()
    '''
'''
def write_records_to_list:
    patients = []
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    while patient_name != '':
        patient_record = []
        patient_age = data_file.readline()
        patient_study = data_file.readline()
        if patient_name not in patient_record:
            patient_record.append(patient_name.rstrip('\n'))
            patient_record.append(patient_age.rstrip('\n'))
            patient_record.append(patient_study.rstrip('\n'))
            if patient_record not in patients:
                patients.append(patient_record)
        patient_name = data_file.readline()
    print(patients)
    data_file.close()
'''


# solution 2 (use 'in' method)
def report_patients_in_more_than_one_study(filename):
    unique_patient = []
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    while patient_name != '':
        patient_age = data_file.readline()
        patient_study = data_file.readline()
        if patient_name not in unique_patient:
            unique_patient.append(patient_name.rstrip('\n'))
        patient_name = data_file.readline()
    data_file.close()

    for patient in unique_patient:
        count = 0
        unique_patient_study_num = []
        data_file = open(filename, 'r')
        patient_name = data_file.readline()
        while patient_name != '':
            patient_age = data_file.readline()
            patient_study = data_file.readline()
            if patient_study != '\n':
                if patient_name.rstrip('\n') == patient:
                    if patient_study not in unique_patient_study_num:
                        unique_patient_study_num.append(patient_study.rstrip('\n'))
                        count += 1
            patient_name = data_file.readline()

        if count > 1:
            print(patient, 'has enrolled in', count, 'different studies')
            print('Study numbers are: ', unique_patient_study_num)
        data_file.close()





# allow user search by patient name
def search_by_name_and_display(filename):
    data_file = open(filename, 'r')
    search = input("Please enter the name of patient you want to search: ")
    found_name = False
    patient_name = data_file.readline()
    while patient_name != '':
        patient_name = patient_name.rstrip()
        if patient_name == search:
            display_certain_record(data_file, patient_name)
            found_name = True
        patient_name = data_file.readline()
    if not found_name:
        print("The name of patient do not exist! ")
    data_file.close()


'''
# am I understand it right? need some work
# The instruction means to find certain patients in a certain age range in a specific study number
# need change the function code
def search_by_age_for_certain_study_number_and_display(filename):
    data_file = open(filename, 'r')
    specific_study_number = input("Please enter the study number of patients you want to search ages for: ")
    patient_name = data_file.readline()
    found_study_num = False
    while patient_name != '':
        if patient_name != '\n':
            patient_age = data_file.readline()
            patient_study = data_file.readline()
            if patient_study.rstrip('\n') == specific_study_number:
                found_study_num = True
                if patient_age != '\n':
                    age = patient_age
                    # read the file from the very beginning
                    read_data_file_again = open(filename, 'r')
                    patient_name_record = read_data_file_again.readline()
                    while patient_name_record != '':
                        if patient_name_record != '\n':
                            patient_age_record = read_data_file_again.readline()
                            patient_study_record = read_data_file_again.readline()
                            if patient_age_record == age:
                                print(patient_name_record.rstrip('\n'))
                                print(patient_age_record.rstrip('\n'))
                                if patient_study_record != '\n':
                                    print(patient_study_record.rstrip('\n'))
                                else:
                                    print(patient_name_record.rstrip('\n'), 'of age', patient_age_record.rstrip('\n'), 'do not have study number')
                        # read the next record
                        patient_name_record = read_data_file_again.readline()
                    read_data_file_again.close()

                else:
                    print(patient_name.rstrip('\n'), 'has the study number of', patient_study.rstrip('\n'), 'but do not has age data')
        patient_name = data_file.readline()
    if not found_study_num:
        print('patient record of', specific_study_number, 'is not exist!')
    data_file.close()
    '''


def search_in_agerange_in_specific_study(filename):
    found = False
    study_num = input("Enter the study number: ")
    print('please enter the range of age you want to search for: ')
    age_max = check_and_add_age()
    age_min = check_and_add_age()
    if age_max < age_min:
        age = age_max
        age_max = age_min
        age_min = age
    data_file = open(filename, 'r')
    patient_name = data_file.readline()
    while patient_name != '':
        patient_age = data_file.readline()
        patient_study = data_file.readline()
        if patient_study.rstrip('\n') == study_num:
            age = int(patient_age)
            if (age <= age_max) and (age >= age_min):
                print('The record is: ', patient_name.rstrip('\n'), patient_age.rstrip('\n'), patient_study.rstrip('\n'))
                found = True
        patient_name = data_file.readline()
    if not found:
        print('The record in study number', study_num, 'can not be found!')
    data_file.close()





def present_options_and_validate():
    filename = open_and_validate_file()
    continue_loop = True
    while continue_loop:
        print("Here is a menu of ten options: ")
        print("1 Add a patient record")
        print("2 Delete a patient record")
        print("3 Count the number of patients in a specific study")
        print("4 Display the patients in a specific study")
        print("5 Detect and correct errors in a specific study")
        print("6 Report all unique study number and patient enrolled in the study")
        print("7 Report all patients who are in more than one study")
        print("8 Search for patient records by name and display")
        print("9 Search for patient records in age range for a specific study and display")
        print("0 Quit")
        instruction_not_valid = True
        while instruction_not_valid:
            user_instruction = input("Please enter the number of the description to start: ")
            if user_instruction == '1' or user_instruction == '2' or user_instruction == '3' or user_instruction == '4' \
                    or user_instruction == '5' or user_instruction == '6' or user_instruction == '7' or user_instruction == '8' \
                    or user_instruction == '9' or user_instruction == '0':
                instruction_not_valid = False
            if user_instruction == '1':
                add_a_patient_record(filename)
            elif user_instruction == '2':
                delete_a_patient_record(filename)
            elif user_instruction == '3':
                study_num = input("Please enter the study number you want to count patients: ")
                count_num_of_patient_in_specific_study(filename, study_num)
            elif user_instruction == '4':
                study_num = input("Please enter the study number you want to count patients: ")
                display_patients_in_specific_study(filename, study_num)
            elif user_instruction == '5':
                detect_and_correct_records(filename)
            elif user_instruction == '6':
                report_unique_study_numbers(filename)
            elif user_instruction == '7':
                report_patients_in_more_than_one_study(filename)
            elif user_instruction == '8':
                search_by_name_and_display(filename)
            elif user_instruction == '9':
                search_in_agerange_in_specific_study(filename)
            elif user_instruction == '0':
                continue_loop = False
        print('')


def main():
    present_options_and_validate()


main()

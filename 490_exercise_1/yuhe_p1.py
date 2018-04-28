#import required module
import re
import string


#store stopwords in a list
def get_stopwords(filename):
    stopwords = []
    for line in filename:
        stopwords.append(line.strip('\n'))
    return stopwords


#check whether there is title in current line
def check_title(line):
    title = ''
    for word in line.split():
        #check whether the word in upper case
        if word.isupper():
            title += word +' '
            continue
        #not title if there is a word in lower case
        else:
            return False, ''
    #title if all of the words in this line in upper case
    return True, title.strip(' ')


#build the index of all the words in the file
def build_index(stories_file, stopwords_file):
    #build the outer index word to stories as w2s
    w2s = dict()
    #build line index
    file_lines = dict()
    #tag the line number from 124
    i = 124
    #stopwords list
    stopwords = get_stopwords(stopwords_file)
    
    #move pointer to line 124
    for m in range(i):
        line = stories_file.readline()
        
    #read from line 124
    while line != '*****\n':
        #index each line with line number
        file_lines[i] = line.strip('\n')
        #go to next loop if line is empty
        if line == '\n':
            i += 1
            line = stories_file.readline()
            continue
        line = re.sub(r'[^a-zA-Z0-9 ]','',line)
        isTitle, title= check_title(line)
        if isTitle:
            story_title = title
            
            #not index title
            i += 1
            line = stories_file.readline()
            continue
        
        for word in line.split():
            #go to next loop if it is stopword
            word = word.lower()
            if word in stopwords:
                continue
            
            word = word.strip(string.punctuation + string.whitespace)
            #use setdefault to make it simple
            w2s.setdefault(word,{}).setdefault(story_title,[i])
            #if i not in w2s[word][story_title]:
            w2s[word][story_title].append(i)
                  
        i += 1
        line = stories_file.readline()

    return w2s, file_lines


#case 1: only one query word
def print_pattern_one(query,w2s,file_lines):
    #deal with query if in the book
    if query in w2s.keys():
        for story in w2s[query].keys():
            
            #print story name with indentation
            print('{:<5}'.format(' '), end = '')
            print(story)
            
            #print story lines that contain the query word
            for num in set(w2s[query][story]):
                #indentation
                print('{:<7}'.format(' '), end = '')
                print(num, end=' ')
                #replace search query in **[A-Z]** format
                line = file_lines[num].replace(query,'**'+query.upper()+'**')
                print(line)
                
    #deal with query if not in the book
    else:
        print('{:<4}'.format(' '), end = '')
        print('--')


#case 2: morethan query with only three words
def print_pattern_morethan(query_list, w2s):
    # build index of stories and their times appear
    def find_words_nums(query, w2s):
        query_in_stories = dict()
        if query in w2s.keys():
            for story in w2s[query]:
                query_in_stories[story] = len(w2s[query][story])
        return query_in_stories
        
    first_word, second_word = query_list[0], query_list[1]
    first_word_in_stories = find_words_nums(first_word, w2s)
    no_story = True

    # if the second word is a number
    if second_word.isdigit():
        second_word_nums = int(second_word)
        for story, nums in first_word_in_stories.items():
            if nums > second_word_nums:
                no_story = False
                print('{:<5}'.format(' '), end = '')
                print(story)
                
    # if the second word is not a number，
    # build index of stories that second word appears
    else:
        second_word_in_stories = find_words_nums(second_word, w2s)
        for story, nums in first_word_in_stories.items():
            if nums > second_word_in_stories.get(story,0):
                no_story = False
                print('{:<5}'.format(' '), end = '')
                print(story)
                
    # if no story satisfy， print --               
    if(no_story):
        print('{:<4}'.format(' '), end = '')
        print('--')


#case 3： near query with only three words
def print_pattern_near(query_list,w2s, file_lines):
    first_word, second_word = query_list[0], query_list[1]
    stories = set()
    no_story = True
    # for every story that first word appear，
    # check whether second word appear at the same line or plus or minus one line
    if first_word in w2s.keys():
        for story in w2s[first_word]:
            for line in set(w2s[first_word][story]):
                lines_to_match = file_lines[line-1]+' '+file_lines[line]+' '+file_lines[line+1]
                # if satisfy， add to the stories set
                if second_word in lines_to_match:
                    no_story = False
                    stories.add(story)
                    
    # if no story satify， print --
    if(no_story):
        print('{:<4}'.format(' '), end = '')
        print('--')
    # print all the stories
    else:
        for story in stories:
            print('{:<5}'.format(' '), end = '')
            print(story)
                
#case 4, 5: multiple query words with 'or' 'and' relation
def print_pattern_or_and(query_list, stories, w2s, file_lines):
    if len(stories) == 0:
        print('{:<4}'.format(' '), end = '')
        print('--')
    #print story name with indentation
    for story in stories:
        print('{:<5}'.format(' '), end = '')
        print(story)

        #print all the query words
        for query in query_list:
            print('{:<7}'.format(' '), end = '')
            print(query)

            #deal with query if not in the book
            if query not in w2s.keys():
                print('{:<8}'.format(' '), end = '')
                print('--')
                continue

            #deal with query in the book and in the this story
            if story in w2s[query].keys():
                for num in set(w2s[query][story]):
                    print('{:<9}'.format(' '), end = '')
                    print(num, end=' ')
                    line = file_lines[num].replace(query,'**'+query.upper()+'**')
                    print(line)
            #deal with query in the book but not in this story
            else:
                print('{:<8}'.format(' '), end = '')
                print('--')
                       

#find query format
def check_query_format(query):
    query_pattern = ''
    query_list = query.split(' ')

    #case 1: only one query word
    if len(query_list) == 1:
        query_pattern = 'one'
        
    #case 2: word more than word, word more than number
    #only allow three words query of morethan. 
    elif (len(query_list) == 3) and ('morethan' in query_list):
        query_pattern = 'morethan'
        query_list.remove('morethan')

    #case 3： word near word
    elif (len(query_list) == 3) and ('near' in query_list):
        query_pattern = 'near'
        query_list.remove('near')
        
    #case 4: 'or' between query words
    elif 'or' in query_list:
        query_pattern = 'or'
        while 'or' in query_list:
            query_list.remove('or')
            
    #case 5: 'and' between query words
    elif 'and' in query_list:
        query_pattern = 'and'
        while 'and' in query_list:
            query_list.remove('and')
    #case 5: implicit 'and ' with only white space between query words
    else:
        query_pattern = 'and'
    return query_list, query_pattern


def search_process():
    #open the two files
    stories_file = open('grimms.txt', encoding = 'utf-8')
    stopwords_file = open('stopwords.txt', encoding = 'utf-8')
    w2s, file_lines = build_index(stories_file, stopwords_file)
    stories_file.close()
    stopwords_file.close()

    print("Welcome to the Grimms'Fairy Tales search system!")
    query = input("Please enter your query: ")
    while query != 'qquit':
        print('')
        print("query = ", query)
        query = query.lower()
        query_list, query_pattern = check_query_format(query)
    
        #case 1: only on query word
        if query_pattern == 'one':
            print_pattern_one(query,w2s,file_lines)

        #case 2: query with keyword 'morethan'
        elif query_pattern == 'morethan':
            print_pattern_morethan(query_list, w2s)

        #case 3: query with keyword 'near'
        elif query_pattern == 'near':
            print_pattern_near(query_list,w2s, file_lines)

        #case 4: more than one query word with 'or' relation
        elif query_pattern == 'or':
            #find all stories that contain at least one of the query
            stories = set()
            for query in query_list:
                if query in w2s.keys():
                    for story in w2s[query].keys():
                        stories.add(story)
                        
            print_pattern_or_and(query_list, stories, w2s, file_lines)

        #case 5: more than one query word with 'and' relation
        elif query_pattern == 'and':
        
            #find all stories that contain at least one of the query
            query_stories = set()
            for query in query_list:
                if query not in w2s.keys():
                    print('{:<4}'.format(' '), end = '')
                    print('--')
                    query_stories = ()
                    break
                else:
                    for story in w2s[query].keys():
                        query_stories.add(story)

            #find stories that contain all the query words 
            if(len(query_stories) != 0):
                stories = set()
                for story in query_stories:
                    story_in_all = True
                    for query in query_list:
                        if story not in w2s[query].keys():
                            story_in_all = False
                    if story_in_all == True:
                        stories.add(story)
    
                print_pattern_or_and(query_list, stories, w2s, file_lines)
    
        #ask user to input query again                           
        query = input("Please enter your query: ")
    
if __name__ == '__main__':
    search_process()

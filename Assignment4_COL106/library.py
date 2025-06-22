import hash_table as ht


class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        
        self.number_of_books=len(book_titles)
        self.book_text_tuple=[]
        for i in range(len(book_titles)):
            sorted_text=self.merge_sort(texts[i])
            distinct_text=[]
            if sorted_text:
                distinct_text.append(sorted_text[0])
            for j in range(1,len(sorted_text)):
                if sorted_text[j]!=sorted_text[j-1]:
                    distinct_text.append(sorted_text[j])
            self.book_text_tuple.append((book_titles[i],distinct_text))
        self.book_text_tuple=self.merge_sort(self.book_text_tuple)
    def distinct_words(self, book_title):
        left=0
        right=self.number_of_books-1
        while left<=right:
            mid=(left+right)//2
            if self.book_text_tuple[mid][0]==book_title:
                # mid corresponds to the same book_title in distinct_texts list
                return self.book_text_tuple[mid][1]
            elif self.book_text_tuple[mid][0]<book_title:
                left=mid+1
            else:
                right=mid-1
    
    def count_distinct_words(self, book_title):
        left=0
        right=self.number_of_books-1
        while left<=right:
            mid=(left+right)//2
            if self.book_text_tuple[mid][0]==book_title:
                # mid corresponds to the same book_title in distinct_text_length list
                return len(self.book_text_tuple[mid][1])
            elif self.book_text_tuple[mid][0]<book_title:
                left=mid+1
            else:
                right=mid-1
    
    def search_keyword(self, keyword):
        selected_titles=[]
        for i in range(self.number_of_books):
            left=0
            right=len(self.book_text_tuple[i][1])-1
            while left<=right:
                mid=(left+right)//2
                if self.book_text_tuple[i][1][mid]==keyword:
                    selected_titles.append(self.book_text_tuple[i][0])
                    break
                elif self.book_text_tuple[i][1][mid]<keyword:
                    left=mid+1
                else:
                    right=mid-1

        return selected_titles
    
    def print_books(self):
        for i in range(self.number_of_books):
            print(f"{self.book_text_tuple[i][0]}:",end="")
            for j in range(len(self.book_text_tuple[i][1])):
                if j!=len(self.book_text_tuple[i][1])-1:
                    print(f" {self.book_text_tuple[i][1][j]} |",end="")
                else:
                    print(f" {self.book_text_tuple[i][1][j]}")

    def merge_sort(self,word_list):
        # Base case: a word_list of 0 or 1 word_list is already sorted
        if len(word_list) <= 1:
            return word_list
        
        # Recursive case: split the word_list in half and sort each half
        mid = len(word_list) // 2
        left_half = self.merge_sort(word_list[:mid])
        right_half = self.merge_sort(word_list[mid:])
        # Merge the two sorted halves together
        return self.merge(left_half, right_half)

    def merge(self,left, right):
        sorted_list = []
        i = j = 0
        
        # Merge elements from both lists into sorted_list
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:  # Lexicographical comparison
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        
        # Append remaining elements, if any
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        
        return sorted_list

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):

        self.params=params
        if name == "Jobs":
            self.method = "Chain"
        elif name == "Gates":
            self.method = "Linear"
        else:
            self.method = "Double"
        self.hashmap_valhashset = ht.HashMap(self.method, params)
        self.hashmap_vallist=ht.HashMap(self.method,params)
        self.hashmap_number_of_distinct=ht.HashMap(self.method,params)
        self.number_of_books=0
        self.book_titles=[]
    def add_book(self, book_title, text):
        # Making the book_title as the key and the text as the value
        self.hashmap_valhashset.insert((book_title,ht.HashSet(self.method,self.params)))
        hashset=self.hashmap_valhashset.find(book_title)
        for i in range(len(text)):
            hashset.insert(text[i])
        distinct_list=[]
        if self.method!="Chain":
            for element in hashset:
                if element!=None:
                    distinct_list.append(element)
        else:
            for bucket in hashset:
                if bucket!=None:
                    for element in bucket:
                        distinct_list.append(element)
                        
        self.hashmap_vallist.insert((book_title,distinct_list))
        self.hashmap_number_of_distinct.insert((book_title,hashset.number_of_keys))
        self.number_of_books+=1
        self.book_titles.append(book_title)

    def distinct_words(self, book_title):
        return self.hashmap_vallist.find(book_title)
    
    def count_distinct_words(self, book_title):
        return self.hashmap_number_of_distinct.find(book_title)
    
    def search_keyword(self, keyword):
        selected_book_titles=[]
        for i in range(self.number_of_books):
            hashset=self.hashmap_valhashset.find(self.book_titles[i])
            if hashset.find(keyword):
                selected_book_titles.append(self.book_titles[i])
        return selected_book_titles
    
    def print_books(self):
        for i in range(self.number_of_books):
            print(f"{self.book_titles[i]}: ",end='')
            print(self.hashmap_valhashset.find(self.book_titles[i]))
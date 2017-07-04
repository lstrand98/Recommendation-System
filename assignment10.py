#Lauren Strand, Karthik, Assignment 10


#Part 1
def read_books(file_name):
	try:
		datafile = open(file_name, "r")
	except:
		return 
		#if file cannot be opened
	books = {}
	#defining dictionary 
	index = 0
	try:
		for data in datafile.readlines():
			#read file
			data = data.strip()
			#strip white spaces
			f = data.split(',')
			#split on the commas
			f.reverse()
			#save in reverse order 
			books[index] = f
			#save count/index as key, title and author as value
			index = index +1
	except:
		return None 
	return books
		#return dictionary 

def read_users(file_name):
	try: 
		users = {}
		#defining another dictionary 
		with open(file_name, 'r') as f:
			for line in f:
				line = line.strip().split()
				#strip white spaces and split on spaces
				rating = list(map(int, line[1:]))
				#save rating as list of ints, from 1 (after user) to end
				users[line[0]] = rating
				#save user as key, ratings as values
		return users
	except IOError as e:
		return None;
	#key: user id....value: list of ratings


def calculate_average_rating(ratings_dict):
	users = read_users("ratings.txt")
	usernames = users.keys()
	avg = {}


	"""
	r = ratings_dict.keys()
	for i in range(len(ratings_dict[r[0]])):
		total = 0
		count = 0
		for key in ratings_dict:
			if ratings_dict[key][i] != 0:
				count = count + 1
				total = total+ratings_dict[key][i]
		if count == 0:
			avg[i] = 0
		else: 
			avg[i] = float(total)/count

	"""

	for i in range(len(users[usernames[0]])):
		#iterating through users dict
		total = 0
		count = 0
		for key in usernames:
			if ratings_dict[key][i] != 0:
				count = count + 1
				total = total + ratings_dict[key][i]
		if count == 0:
			avg[i] = 0
		else:
			avg[i] = float(total)/count 
			#calculate average as float
	
	return avg 


def lookup_average_rating(index, book_dict, avg_ratings_dict):
	ar = avg_ratings_dict[index]
	bd = book_dict[index]
	bd_t = bd[0]
	bd_a = bd[1]
	format = "(%f) %s by %s"
	return format%(ar, bd_t, bd_a)
	#returning as string in specific format



#Part 2
class Recommender:
	def __init__(self, books_filename, ratings_filename):
		self.Books = {}
		self.Ratings = {}
		self.Average = {}
		self.read_books(books_filename)
		self.read_users(ratings_filename)
		self.calculate_average_rating()

	def read_books(self, file_name):
		try:
			datafile = open(file_name, "r")
		except:
			return 
		index = 0
		try:
			for data in datafile.readlines():
				data = data.strip()
				f = data.split(',')	#.split is a list
				f.reverse()
				self.Books[index] = f
				index = index +1
			
		except:
			return None 
		
		return self.Books

	def read_users(self, user_file):
		try: 
			with open(user_file, 'r') as f:
				for line in f:
					line = line.strip().split()
					rating = list(map(int, line[1:]))
					self.Ratings[line[0]] = rating

		except IOError as e:
			return None;
		
		return self.Ratings

	def calculate_average_rating(self):
		usernames = self.Ratings.keys()

		for i in range(len(self.Ratings[usernames[0]])):
			total = 0
			count = 0
			for key in usernames:
				if self.Ratings[key][i] != 0:
					#0 indicates not read yet
					count = count + 1
					total = total + self.Ratings[key][i]
			if count == 0:
				self.Average[i] = 0

			else:
				#round to 2 decimals
				self.Average[i] = float(total)/count 


	def lookup_average_rating(self, index):
		ar = float(("%.2f" %self.Average[index]))
		#save as value with only 2 decimal values
		bd = self.Books[index]
		bd_t = bd[0]
		bd_a = bd[1]
		format = "(%.2f) %s by %s"
		return format%(ar, bd_t, bd_a)

	def calc_similarity(self, user1, user2):
		product = 0
		similarity = 0
		
		for i in range(len(self.Ratings[user1])):
			product = (self.Ratings[user1][i]) * (self.Ratings[user2][i])
			#multiply those 2 indexes
			similarity = similarity + product
			#calculating similarity (dot product)
		
		return similarity


	def get_most_similar_user(self, current_user_id):
		most_similar = ""
		highest = 0
		users = self.Ratings.keys()

		for user in users:
			if current_user_id != user:
				#don't compare score of user to itself
				s = self.calc_similarity(current_user_id, user)
				if highest<s:
					highest = s
					#bubble sort to find max
					most_similar = user
		return most_similar

	def recommend_books(self, current_user_id):
		m_s = self.get_most_similar_user(current_user_id)
		recommendations = []
		#create list to save all of the recommendations 

		for i in range(len(self.Ratings[m_s])):
			mylist = self.Ratings[m_s]
			if mylist[i] == 3 or mylist[i] ==5:
				if self.Ratings[current_user_id][i] == 0:
					#if rating high or not read yet, add those books to the list
					recommendations.append(self.lookup_average_rating(i))


		return recommendations
		
			






#main

def main():
	#Part 1
	mybooks = read_books("books.txt")
	print mybooks
	print 

	myusers = read_users("ratings.txt")
	print myusers
	#print sorted(myusers.keys()) 
	print 
	
	myaverage = calculate_average_rating(myusers)
	print myaverage
	print 

	mylookup = lookup_average_rating(0, mybooks, myaverage)
	print mylookup

	print 
	print "Part 2"
	print 

	#Part 2
	R = Recommender("books.txt", "ratings.txt")
	R.read_books("books.txt")
	R.read_users("ratings.txt")
	R.calculate_average_rating()
	R.lookup_average_rating(0)


	print R.Books
	print R.Ratings
	print R.Average

	print "calc similarity test : "
	score = R.calc_similarity("Cust8", "Shannon")
	print score 
	print 

	print R.lookup_average_rating(13)
	print 

	ms = R.get_most_similar_user("Rudy.A")
	print ms 
	print

	rec = R.recommend_books("Ella")
	print rec


if __name__ == '__main__':
	main()
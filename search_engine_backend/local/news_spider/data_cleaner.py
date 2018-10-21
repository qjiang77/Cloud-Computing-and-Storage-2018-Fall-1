import os

if __name__ == "__main__":
	article_dir = os.path.join(os.path.dirname(__file__), "articles")
	for subdir in os.listdir(article_dir):
		article_subdir = os.path.join(article_dir, subdir)
		num_files = len(os.listdir(article_subdir))
		#print(os.listdir(article_subdir))
		#input()
		if num_files == 0: # On Windows, listdir() will always return a list with at least 2 elements, '.' and '..'; while on Linux, listdir() will not include these two elements.
			os.rmdir(article_subdir) # empty folder needed to be removed
			print("%s: empty" % subdir)
		else:
			print("%s: %d articles" % (subdir, num_files))


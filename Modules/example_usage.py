from ClassifierInterface import ClassifierInterface, IncomingQueue
from TwitterAgent import TwitterAgent

## needed for this use case only
import threading, time, sys
import numpy as np

## used to avoid priting emoji in IDLE
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

classified = 0
def main():
	ta = TwitterAgent()
	incoming_queue = IncomingQueue()
	c = ClassifierInterface(incoming_queue)
	ready_queue = c.ready_queue
	max_tweets=[-1]
	def stream_task(q):
		# receive a sample of the global tweets stream
		ta.get_sample_tweets_stream(max_tweets=max_tweets, data_handler=q, save_to_files=False)

	def classify_task():
		while(True):
##			time.sleep(0.001)
			c.classify_batch()
			# print classified tweets
			while(ready_queue.qsize()!=0): use_ready_queue(ready_queue)

			# stop after the stream is closed and all tweets are classified
			if (not stream_thread.is_alive() and incoming_queue.qsize()==0): break
		
	stream_thread = threading.Thread(target=stream_task, args = (incoming_queue,))
	stream_thread.start()
	classify_thread = threading.Thread(target=classify_task)
	classify_thread.start()
	
	while(classify_thread.is_alive()):
		print('waiting:{}, ready:{}\n'.format(incoming_queue.qsize(), ready_queue.qsize()))
		
		# stopping the stream from any thread
		if(classified>30):
			max_tweets[0]=0


# An example usage of the classified tweets
sent_map=['Happy','Love','Hopeful','Neutral','Angry','Hopeless','Hate','Sad']
def use_ready_queue(ready_queue):
	global classified; classified+=1
	tweet = ready_queue.get()
	probs=', '.join(['{}: {:.3}'.format(sent_map[l], tweet.sentiment[l]) for l in np.argsort(tweet.sentiment)[::-1][:3] if tweet.sentiment[l]>0.01])
	print('tweet: {}\nprobs: {}\nlocation: {}\n'.format(tweet.text, probs, tweet.location).translate(non_bmp_map))
	

if __name__ == '__main__': main()


'''
Requirements
a config.json file of shape
{
	"data_path": "",
	
	"consumer_key": "",
	"consumer_secret": "",

	"access_token": "",
	"access_token_secret": ""
}

the data_path folder should have the following
1. folder d200_word_embedding
1.1. can be created by extracting the files in the glove file from http://nlp.stanford.edu/data/glove.twitter.27B.zip
into a folder named glove.twitter.27B in the data_path folder
1.2. then running Word_Embeddding_Glove_Saver().run() and choosing embedding dim = 200
2.1. folder Sessions/DefaultSession having a checkpoint of a trained session
or
2.2. folder DataSet with the DataSet's csv files each row of shape link, tweet, label1, label2, label3
	with labels ranging from 0:7
2.2.1. then to train a session
	a. run Classifier()
	b. then Classifier.train()
	c. then Classifier.save_session()
'''

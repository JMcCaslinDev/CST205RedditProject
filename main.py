import praw
import os, re, requests
import json
from PIL import Image




def returnJsonDictObject(filename):#string attribute
  #check if file empty
  if(os.stat(filename).st_size != 0):
    #open json file
    with open(filename, 'r') as access_json:
       #read_content given info from json
      read_content = json.load(access_json)
  #returns dict object 
  return read_content


  
def returnRedditInstance():
    jData = returnJsonDictObject('Credentials.json')
    reddit = praw.Reddit(
        client_id=jData.get('client_id'),
        client_secret=jData.get('client_secret'),
        password=jData.get('password'),
        user_agent=jData.get('user_agent'),
        username=jData.get('username'),)
    return reddit


def downloadImageFromSubreddit(submission):
    url = (submission.url)
    file_name = url.split("/")
    if len(file_name) == 0:
        file_name = re.findall("/(.*?)", url)
    file_name = file_name[-1]
    if "." not in file_name:
        file_name += ".jpg"
    print(file_name)
    r = requests.get(url)
    with open(file_name,"wb") as f:
        f.write(r.content)



def main():
  
  reddit = returnRedditInstance()

  #reddit.subreddit("FreeKarma4You")(new)

  for submission in reddit.subreddit('ImageProccessingCS205').new(limit = 10):
    if "Output" in submission.url:
      continue
      
    print(submission.title)
    choice = submission.title
    url = submission.url
    print(url)
  
    image = returnImageFromUrl(url)

    if (choice == "grayscale"):
      image = grayscale(image)
      title = "Output Grayscale"
      post(image, submission, reddit, title)
      
    elif(choice == "sepia"):
      image = sepia(image)
      title = "Output Sepia"
      post(image, submission, reddit, title)
      
    elif(choice == "negative"):
      image = negative(image)
      title = "Output Negative"
      post(image, submission, reddit, title)

    elif(choice == "scale down"):
      image = scaleDown(image)
      title = "Output scale down"
      post(image, submission, reddit, title)

  
    

  
#end of main

def post(image, submission, reddit,title):
      
      image.save("images/resultImage.png")



  
      
      images = "images/resultImage.png"
      subreddit = reddit.subreddit("ImageProccessingCS205")
      subreddit.validate_on_submit = True
      
      try:
        subreddit.validate_on_submit = True
        subreddit.submit_image(title, images)
        print("post posted!!")
        
      except praw.exceptions.APIException as e:
        #Ratelimit hit when posting path
        print(e)
        print("\nrateLimit posting error need to add time locks \n")

def returnImageFromUrl(url):
  image = Image.open(requests.get(url, stream=True).raw)
  return image
  
#api to pixel function
def conv_pic_to_pix(img):
  im2 = Image.open(requests.get(img, stream=True).raw)
  pix = im2.getdata()
  print(list(pix))
  return pix



#Image filtering functions
def grayscale(img):
  width, height = img.size
  new_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                    for a in img.getdata() ]
  return_image = Image.new('RGB', (width, height))
  return_image.putdata(new_list)
  return return_image


def sepia(img):
    width, height = img.size
    return_image = Image.new('RGB', (width, height))
   # tint shadows
    for a in img.getdata():
      if a[0] < 63:
         sepia_list = [(int(a[0] * 1.1), a[1], int(a[2] * 0.9))]
      
      # tint midtones
      elif a[0] > 62 and a[0] < 192:
         sepia_list = [(int(a[0] * 1.15), a[1], int(a[2] * 0.85))]
      
      # tint highlights
      else:
        r = int(a[0] * 1.08)
        g,b = a[1], int(a[2] * 0.5)
        sepia_list = [(r,g,b)]

      return_image.putdata(sepia_list) #int list 
      sepia_list = 

    return return_image


def negative(img):
  width, height = img.size
  negative_list = [(255-p[0], 255-p[1], 255-p[2])
                            for p in img.getdata()]
  return_image = Image.new('RGB', (width, height))
  return_image.putdata(negative_list)
  return return_image

def scaleDown(img):
    w, h = img.width//2, img.height//2
    return_image = Image.new('RGB', (w, h))
    target_x = 0
    for source_x in range(0, img.width, 2):
        target_y = 0
        for source_y in range(0, img.height, 2):
            p = img.getpixel((source_x, source_y))
            return_image.putpixel((target_x, target_y), p)
            target_y += 1
        target_x += 1
        
    return return_image























#needs to be last line of file
if __name__ == '__main__':
  main()
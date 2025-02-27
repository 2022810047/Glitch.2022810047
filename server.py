from flask import Flask, request, redirect
app = Flask(__name__)
 
 
the_pages = [
  {"id":"1","title":"The First","sentence":"this"},
  {"id":"2","title":"The Second","sentence":"that"},
  {"id":"3","title":"The Third","sentence":"these"}
]


def template(id, up_title=None, up_sentence=None, up_id=None):
    pages = ""
    for page in the_pages:
      pages += f'''
      <li>
        <a href="/read/{page["id"]}/">
          {page["title"]}
        </a>
      </li>\n
      '''
    if id == "create":
      title = "<input type='text' name='title' placeholder='제목을 작성해주세요'>"
      sentence = "<textarea name='sentence' placeholder='내용을 작성해주세요'></textarea>\n<input type='submit' value='완료'>"
      update_button = ""
      delete_button = ""
        
    elif id == "update":
      title = f"<input type='text' name='title' placeholder='{up_title}'>"
      sentence = f"<textarea name='sentence' placeholder='{up_sentence}'></textarea>\n<input type='submit' value='완료'>"
      update_button = ""
      delete_button = ""
    
    else:
      try:
        title = the_pages[id-1]["title"]
        sentence = the_pages[id-1]["sentence"]
        update_button = f"<button type='button' onclick=\"location.href='/update/{id}/'\">글 수정</button>"
        delete_button = f"<form action='/delete/{id}/' method='POST'><input type='submit' value='삭제'></form>"

      except:
        title = "welcome"
        sentence = "made by 2022810047"
        update_button = ""
        delete_button = ""
    
    if up_title != None:
      loader = f"""
        <form action='/update/{up_id}/' method='POST'>
          <h2>{title}</h2>
          <br>
          <p>{sentence}</p>
        </form>
        """
    else:
      loader = f"""
        <form action='/create/' method='POST'>
          <h2>{title}</h2>
          <br>
          <p>{sentence}</p>
        </form>
        """

    
    
    return f"""
    <!doctype html>
    <html>
      <body style="background-color:#92cf8f;">
      <div style="margin:25px; padding:15px; background-color:white; border-radius: 15px;">
        <h1><a href="/" style="color:#92cf8f;">Homepage</a></h1>
        <ul>
          {pages}
        </ul>
        
        <button type="button" onclick="location.href='/create/' ">글 쓰기</button>
        
        <hr>
        {loader}
        {update_button}
        <br>
        {delete_button}
      </div>
      </body>
    </html>
    """



#---------------------------------------------------------------------------------------
@app.route('/')
def home():
    return template(None)
    
 

@app.route('/read/<int:id>/')
def read(id):
    return template(id)
  
  
  
@app.route('/create/', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return template("create")
    elif request.method == 'POST':
        title = request.form["title"]
        sentence = request.form["sentence"]
        new_page = {"id":len(the_pages)+1,"title":title, "sentence":sentence}
        new_id = new_page["id"]
        the_pages.append(new_page)
        the_url = f"/read/{new_id}/"
        return redirect(the_url)
  

  
@app.route('/update/<int:id>/', methods=['GET','POST'])
def update(id):
    if request.method == 'GET':
        title = the_pages[id-1]["title"]
        sentence = the_pages[id-1]["sentence"]
        return template("update", title, sentence, id)
      
    elif request.method == 'POST':
        title = request.form["title"]
        sentence = request.form["sentence"]
        the_pages[id-1]["title"] = title
        the_pages[id-1]["sentence"] = sentence     
        the_url = f"/read/{id}/"
        return redirect(the_url)

      
      
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    del the_pages[id-1]
    return redirect("/")
  
  
  
app.run() 
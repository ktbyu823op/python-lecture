eturn render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}") 
    save_to_file(keyword,db[keyword])
    return send_file(f"{keyword}.csv",as_attachment=True)

app.run("0.0.0.0")

""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor, execute_values

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='prefer')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

## USER STUFF
def add_user(user_id, username):
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding person %s", username)
        cur.execute("INSERT INTO users (u_id, username) values (%s, %s)", (user_id, username))

def get_username(user_id):
     with get_db_cursor(True) as cur:
        cur.execute("SELECT username FROM users WHERE u_id = %s", (user_id,))
        res = cur.fetchone()
        return res['username'] if res else res

def get_uid(username):
     with get_db_cursor(True) as cur:
        cur.execute("SELECT u_id FROM users WHERE username = %s", (username,))
        res = cur.fetchone()
        return res['u_id'] if res else res

def edit_username(user_id, username):
    with get_db_cursor(True) as cur:
        current_app.logger.info("Trying to add %s", username)
        cur.execute("""UPDATE users SET username = %s WHERE u_id = %s""", (username, user_id))

## POST
def get_posts(page = 1, post_per_page = 12):
    ''' note -- result can be used as list of dictionaries'''
    limit = post_per_page
    offset = (page-1)*post_per_page
    with get_db_cursor() as cur:
        cur.execute("select * from posts order by upload_time DESC limit %s offset %s", (limit, offset))
        return cur.fetchall()

def get_post(post_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM posts where post_id=%s", (post_id,))
        return cur.fetchone()

def upload_post(data, title, desc, hint, show_comment, sol, u_id):
    with get_db_cursor(True) as cur:
        cur.execute("""insert into posts (title, post_image,
            descrip, hint, show_comment, solution, author) 
            values (%s, %s, %s, %s, %s, %s, %s) RETURNING post_id""",
            (title, data, desc, hint, show_comment, sol, u_id))
        return cur.fetchone()[0] #postid

def get_image_ids():
    with get_db_cursor() as cur:
        cur.execute("select post_id from posts;")
        return [r['post_id'] for r in cur]

def edit_post(title, desc, hint, show_comment, post_id):
    with get_db_cursor(True) as cur:
        current_app.logger.info("Trying to edit %s", post_id)
        cur.execute("""UPDATE posts SET title = %s, descrip = %s, 
            hint = %s, show_comment = %s WHERE post_id = %s""", 
            (title, desc, hint, show_comment, post_id))

def delete_post(post_id):
     with get_db_cursor(True) as cur:
        current_app.logger.info("Trying to delete %s", post_id)
        cur.execute("""DELETE FROM posts WHERE post_id = %s""", (post_id,))

def delete_comment(comment_id):
     with get_db_cursor(True) as cur:
        current_app.logger.info("Trying to delete comment with id: %s", comment_id)
        cur.execute("""DELETE FROM COMMENTS WHERE comment_id = %s""", (comment_id,))

def mark_post_solved(solved, post_id):
    with get_db_cursor(True) as cur:
        cur.execute("""UPDATE posts SET solved = %s WHERE post_id = %s""", 
            (solved, post_id))

## TAGS
def get_tags(post_ids=[]):
    with get_db_cursor() as cur:
        if post_ids == []:
            cur.execute("""
                SELECT post_id, title, textcat_all(tag_name || ',') 
                FROM(
                    SELECT * FROM 
                        (SELECT * FROM posts 
                        LEFT JOIN tagged ON post_id=post) 
                    AS joinedTags LEFT JOIN tags ON tag=tag_id) 
                AS tag_labels 
                GROUP BY post_id, title, upload_time ORDER BY upload_time DESC;""")
        else:
            cur.execute("""
                SELECT post_id, textcat_all(tag_name || ',') 
                FROM(
                    SELECT * FROM 
                        (SELECT * FROM posts 
                        LEFT JOIN tagged ON post_id=post WHERE post_id = ANY (%s)) 
                    AS joinedTags LEFT JOIN tags ON tag=tag_id) 
                AS tag_labels 
                GROUP BY post_id, upload_time ORDER BY upload_time DESC;""", 
                (post_ids,))
        return cur.fetchall()

def get_tag(post_id):
    with get_db_cursor() as cur:
        # This is kinda bad, definitely optimize this by adding WHERE clause deeper in query
        cur.execute("""SELECT post_id, textcat_all(tag_name || ',') 
            FROM(
                SELECT * FROM 
                    (SELECT * FROM posts 
                    LEFT JOIN tagged ON post_id=post) 
                AS joinedTags LEFT JOIN tags ON tag=tag_id) 
            AS tag_labels  WHERE post_id=%s 
            GROUP BY post_id ORDER BY post_id;""", (post_id,)) 
        return cur.fetchone()

def get_all_tags():
    with get_db_cursor() as cur:
        cur.execute("SELECT * from tags;")
        return cur.fetchall()

def tag_post(tags, post_id):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT tag_id from tags WHERE tag_name = ANY (%s)", (tags,) )
        data = [(post_id, t['tag_id']) for t in cur.fetchall()]
        execute_values(cur, "INSERT INTO tagged (post, tag) VALUES %s", data)


## VIEWING MULTIPLE POSTS
def get_total_post_ids():
    with get_db_cursor() as cur:
        cur.execute("SELECT MAX(post_id) from posts;")
        return cur.fetchall()

def get_num_of_posts():
    with get_db_cursor() as cur:
        cur.execute("select COUNT(*) from posts")
        return cur.fetchone()[0]

def get_post_author_name(post_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT post_id, username FROM( SELECT * FROM users LEFT JOIN posts ON u_id=author) AS usernameTag WHERE post_id=%s;", (post_id,)) 
        return cur.fetchall()

def get_posts_by_author(u_id):
    with get_db_cursor() as cur:
        cur.execute("""SELECT * FROM posts WHERE author = %s ORDER BY upload_time DESC""", (u_id,))
        return cur.fetchall()

## COMMENTS
def add_comment(post_id, author, content):
    with get_db_cursor(True) as cur:
        cur.execute("""INSERT INTO comments (post, author, content)
            vALUES (%s, %s, %s) RETURNING comment_id""", 
            (post_id, author, content))
        return cur.fetchone()[0] #comment_id

def get_comments(post_id):
    with get_db_cursor() as cur:
        cur.execute("""SELECT * FROM comments LEFT JOIN users ON u_id = author
             WHERE post = %s""", (post_id,))
        return cur.fetchall()

def get_comment_details(comment_id):
    with get_db_cursor() as cur:
        cur.execute("""SELECT * FROM comments LEFT JOIN users ON u_id = author
             WHERE comment_id = %s""", (comment_id,))
        return cur.fetchall()

def get_comment_counts(post_ids):
    with get_db_cursor() as cur:
        cur.execute("""
           SELECT count(comments.post) as number_of_comments
            from posts left join comments on posts.post_id = comments.post
            WHERE post_id = ANY (%s)
            GROUP BY posts.post_id ORDER BY posts.upload_time DESC""", 
            (post_ids, ))
        return [c[0] for c in cur.fetchall()]

# SEARCH 
        
def get_search(query, tags='all'):
    with get_db_cursor() as cur:
        if tags == 'all':
            cur.execute("""SELECT * 
            FROM posts 
            WHERE title @@ to_tsquery(%s) OR descrip @@ to_tsquery(%s)
            order by upload_time DESC""", (query, query))
        else:
            cur.execute("""SELECT p.* 
            FROM posts p, tags t, tagged tp
            WHERE tp.tag = t.tag_id
            AND (p.title @@ to_tsquery(%s) OR p.descrip @@ to_tsquery(%s))
            AND t.tag_name = (%s)
            AND p.post_id = tp.post
            GROUP BY p.post_id
            ORDER BY upload_time DESC""", (query, query, tags,))
            #current_app.logger.info(f"searching by tags: " + str(tags))
        return cur.fetchall()

def get_search_tag_only(tags=[]):
     with get_db_cursor() as cur:
        current_app.logger.info(f"searching by tags: " + str(tags))
        if tags == []:
            cur.execute("""SELECT * FROM posts order by upload_time DESC""",)
        else:
            cur.execute("""SELECT p.* 
            FROM posts p, tags t, tagged tp
            WHERE tp.tag = t.tag_id
            AND t.tag_name = (%s)
            AND p.post_id = tp.post
            GROUP BY p.post_id
            ORDER BY upload_time DESC""", (tags,))
        return cur.fetchall()
Let's say we have this code:

```python
authors = Author.objects.all()

# Loop through authors and access their books
for author in authors:
    print(f"{author.name}'s books:")
    for book in author.books.all():  # This triggers a new query each time!
        print(f"- {book.title}")
```

1. **Initial query**: First, Django executes a query to get all authors:

    ```SQL
    SELECT id, name FROM author;
    ```

    And expect it to return two authors: J.K. Rowling (id=1) and George Orwell (id=2)

2. **First iteration - J.K. Rowling:**: When we access author.books.all() for the first author, Django executes:

    ```SQL
    SELECT id, title, author_id FROM book WHERE author_id = 1;
    ```

3. **Second iteration - George Orwell**: When we access author.books.all() for the second author, Django executes:

    ```SQL
    SELECT id, title, author_id FROM book WHERE author_id = 2;
    ```

So we executed 3 separate database queries:

-   The `n` is the total objects we need to get, here is the `author`
-   The `+1` is the first query: getting all of them

**With techniques such as using `prefetch_related`, we're able to massively increase the performance.**

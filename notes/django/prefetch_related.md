# `prefetch_related`

`prefetch_related` is designed to improve performance when retrieving related objects in a Django query, particularly for many-to-many relationships or reverse foreign key relationships.

When execute `prefetch_related`:

1. Django executes a separate query for each relationship we're prefetching
2. It then joins the results in Python rather than in the database
3. This helps prevent the "N+1 queries problem" where we might otherwise execute a new database query for each related object

## Use Case

Let's imagine we have a blog application with two models: Author and Book (where an author can write multiple books).

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

When we use `prefetch_related`

```python
authors = Author.objects.prefetch_related('books').all()
```

_What happens is:_

1. **First query execution**: Django first executes a query to get all authors:

    ```SQL
    SELECT id, name FROM author;
    ```

    This will return data like:

    ```
    id | name
    ---+------------
    1  | J.K. Rowling
    2  | George Orwell
    ```

2. **Collection of primary keys**: Django collects all the primary keys from the authors:

    ```
    [1, 2]
    ```

3. **Second query with filter**: Django then executes a second query to fetch all books related to these authors in one go:

    ```sql
    SELECT id, title, author_id FROM book WHERE author_id IN (1, 2);
    ```

    And this could return:

    ```
    id | title          | author_id
    ---+----------------+----------
    1  | Harry Potter   | 1
    2  | Fantastic Beasts| 1
    3  | 1984           | 2
    4  | Animal Farm    | 2
    ```

4. **In-memory joining:** Django now performs an in-memory operation to organize these books by author_id:

    ```python
    {
        1: [Book(id=1, title='Harry Potter'), Book(id=2, title='Fantastic Beasts')],
        2: [Book(id=3, title='1984'), Book(id=4, title='Animal Farm')]
    }
    ```

5. **Caching**: Django attaches these pre-fetched books to each author object in its internal cache.

6. **Query avoidance**: Now when you loop through authors and access their books, no additional queries are executed because Django uses the pre-fetched data from its cache.

    ```python
    for author in authors:
        print(f"{author.name}'s books:")
        for book in author.books.all():  # No additional query!
            print(f"- {book.title}")
    ```

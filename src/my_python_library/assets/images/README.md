Put ticket images here.

Example filename:

```text
ticket_6_question_3.png
```

Then add a link in `src/my_python_library/images.py`:

```python
TICKET_IMAGES = {
    6: (
        TicketImage(6, 3, "ticket_6_question_3.png", "Форма для задания"),
    ),
}
```

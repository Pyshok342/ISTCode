Put ticket files here.

Supported examples:

```text
ticket_6_form.png
ticket_6_presentation.pptx
ticket_10_schema.pdf
ticket_12_table.xlsx
```

Then add links in `src/my_python_library/files.py`:

```python
TICKET_FILES = {
    6: (
        TicketFile(6, 3, "ticket_6_form.png", "Форма для задания"),
        TicketFile(6, 3, "ticket_6_presentation.pptx", "Презентация"),
    ),
}
```

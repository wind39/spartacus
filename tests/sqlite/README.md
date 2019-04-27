### Starting

```
cd spartacus/Spartacus/tests/sqlite
gunzip -k ../../samples/employees.db.gz -c > employees.db
```

### Testing

```
python test_sqlite.py
```

### Finishing

```
rm employees.db
```

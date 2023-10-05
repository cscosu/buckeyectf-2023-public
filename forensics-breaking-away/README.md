# forensics-breaking-away

`dist/forensics-breaking-away.pdf` is a PDF file with hidden metadata.

1. Search through PDF metadata to find reference to `3.225.42.93` IP
2. Reverse DNS `3.225.42.93` to find URL `mymostfavouritesongsofalltime.net` DNS entry.
3. Subdomain brute forcer to find s3 bucket subdomain `mymostfavouritesongsofalltime`
    4. `amass` is able to find `admin.mymostfavouritesongsofalltime.net` when brute-force is enabled.
5. Search through `users.html` to find flag, base-64 encoded. Can quickly find via searching for `=` on page.
6. Unencode flag, listed in /users.html
import argparse
import os
from typing import Optional

from app.database import SessionLocal
from .md_importer import import_directory, import_markdown_file


def main(argv: Optional[list] = None):
    parser = argparse.ArgumentParser(description='Import Markdown knowledge points into the database')
    parser.add_argument('--dir', dest='dir', help='Directory containing .md files (non-recursive)')
    parser.add_argument('--file', dest='file', help='Single .md file to import')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing title if exists')
    args = parser.parse_args(argv)

    if not args.dir and not args.file:
        parser.error('Please provide --dir or --file')

    db = SessionLocal()
    try:
        if args.file:
            if not os.path.isfile(args.file):
                raise SystemExit(f'File not found: {args.file}')
            status, obj = import_markdown_file(db, args.file, overwrite=args.overwrite)
            print({
                'file': os.path.basename(args.file),
                'status': status,
                'id': getattr(obj, 'id', None),
                'title': getattr(obj, 'title', None),
            })
        else:
            if not os.path.isdir(args.dir):
                raise SystemExit(f'Directory not found: {args.dir}')
            results = import_directory(db, args.dir, overwrite=args.overwrite)
            created = sum(1 for r in results if r['status']=='created')
            updated = sum(1 for r in results if r['status']=='updated')
            skipped = sum(1 for r in results if r['status']=='skipped')
            failed = sum(1 for r in results if r['status']=='failed')
            print({'created': created, 'updated': updated, 'skipped': skipped, 'failed': failed})
            for r in results:
                print(r)
    finally:
        db.close()


if __name__ == '__main__':
    main()
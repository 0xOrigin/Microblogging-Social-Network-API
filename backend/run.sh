#!/bin/bash

# Colors
RED='\033[0;31m'
Green='\033[0;32m'
NC='\e[0m'

BOLD_RED='\033[1;31m'
BOLD_GREEN='\033[1;32m'

# Define the valid option and its argument
valid_option="t:s"

# Parse arguments using getopts
while getopts ${valid_option} flag; do
    case ${flag} in
        t)
            target="$OPTARG"
            ;;
        s)
            setup=true
            ;;
        \?)
            exit 1
            ;;
        *)
            exit 1
            ;;
    esac
done


if [ "$setup" = true ]; then
    pip install --upgrade pip
    pip install --no-cache-dir --no-cache -r ./requirements.txt || echo -e "${BOLD_RED}[!] Failed to install dependencies!${NC}"
    pip cache purge
fi


# Check the target value
if [ "$target" = "production" ]; then
    # Remove the cache files
    find . -path "*/__pycache__/*pyc" -delete
    find . -path "*/__pycache__" -delete

    # Collect static files
    python manage.py collectstatic --noinput || echo -e "${BOLD_RED}[!] Failed to collect static files!${NC}"

    # Compile translation files
    # python manage.py compilemessages || echo -e "${BOLD_RED}[!] Failed to compile translation files!${NC}"

    # Make migrations
    python manage.py makemigrations --noinput || echo -e "${BOLD_RED}[!] Failed to make migrations!${NC}"

    # Apply database migrations
    python manage.py migrate || echo -e "${BOLD_RED}[!] Failed to apply database migrations!${NC}"

    # Run the Django production server
    gunicorn backend.wsgi:application -b 0.0.0.0:$BACKEND_DEV_PORT

elif [ "$target" = "development" ]; then
    # Remove the cache files
    find . -path "*/__pycache__/*pyc" -delete
    find . -path "*/__pycache__" -delete

    # Collect static files
    python manage.py collectstatic --noinput || echo -e "${BOLD_RED}[!] Failed to collect static files!${NC}"

    # Compile translation files
    # python manage.py compilemessages || echo -e "${BOLD_RED}[!] Failed to compile translation files!${NC}"

    # Make migrations
    python manage.py makemigrations --noinput || echo -e "${BOLD_RED}[!] Failed to make migrations!${NC}"

    # Apply database migrations
    python manage.py migrate || echo -e "${BOLD_RED}[!] Failed to apply database migrations!${NC}"

    # Run the Django development server
    gunicorn backend.wsgi:application -b 0.0.0.0:$BACKEND_DEV_PORT --reload
fi

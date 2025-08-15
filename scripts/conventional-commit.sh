#!/bin/bash

# An interactive script to guide the user in creating a Conventional Commit.

set -e

# --- Stage all changes ---
git add .
printf "✓ All changes have been staged for commit.\n\n"

# --- 1. Choose the Type ---
printf "1. Select the type of change you're committing:\n"
options=("feat:     A new feature" "fix:      A bug fix" "chore:    Build process or auxiliary tool changes" "docs:     Documentation only changes" "style:    Changes that do not affect the meaning of the code" "refactor: A code change that neither fixes a bug nor adds a feature" "perf:     A code change that improves performance" "test:     Adding missing tests or correcting existing tests" "build:    Changes that affect the build system or external dependencies" "ci:       Changes to our CI configuration files and scripts")

select opt in "${options[@]}"; do
    TYPE=$(echo "$opt" | cut -d':' -f1)
    if [ -n "$TYPE" ]; then
        break
    else
        echo "Invalid option. Please try again."
    fi
done

# --- 2. Enter the Scope ---
printf "\n2. What is the scope of this change (e.g., component or file name)? (press enter to skip)\n"
read -r SCOPE_INPUT
SCOPE=""
if [ -n "$SCOPE_INPUT" ]; then
    SCOPE="($SCOPE_INPUT)"
fi

# --- 3. Enter the Description ---
while true; do
    printf "\n3. Write a short, imperative tense description of the change:\n"
    read -r DESCRIPTION
    if [ -n "$DESCRIPTION" ]; then
        break
    else
        printf "✗ Description cannot be empty.\n"
    fi
done

# --- 4. Enter the Body ---
printf "\n4. Provide a longer description of the change (optional, press Ctrl+D when done):\n"
BODY=$(cat)

# --- 5. Breaking Changes ---
IS_BREAKING=""
BREAKING_FOOTER=""
while true; do
    printf "\n5. Is this a BREAKING CHANGE? (y/n)\n"
    read -r answer
    case $answer in
        [Yy]* ) 
            IS_BREAKING="!"
            printf "\nPlease describe the breaking change:\n"
            read -r BREAKING_DESCRIPTION
            BREAKING_FOOTER="BREAKING CHANGE: ${BREAKING_DESCRIPTION}"
            break
            ;; 
        [Nn]* ) 
            break
            ;; 
        * ) 
            printf "✗ Please answer yes or no.\n"
            ;; 
    esac
done

# --- Assemble the commit message ---
SUBJECT="${TYPE}${SCOPE}${IS_BREAKING}: ${DESCRIPTION}"
FULL_BODY=""

if [ -n "$BODY" ]; then
    FULL_BODY+="$BODY"
fi

if [ -n "$BREAKING_FOOTER" ]; then
    # Add a blank line between body and footer if body exists
    if [ -n "$FULL_BODY" ]; then
        FULL_BODY+="\n\n"
    fi
    FULL_BODY+="$BREAKING_FOOTER"
fi

# --- Execute the commit ---
printf "\nCommitting with the following message:\n"
printf -- "-------------------------------------
"
printf "%s\n" "$SUBJECT"
if [ -n "$FULL_BODY" ]; then
    printf "\n%s\n" "$FULL_BODY"
fi
printf -- "-------------------------------------
"

if [ -n "$FULL_BODY" ]; then
    git commit -m "$SUBJECT" -m "$FULL_BODY"
else
    git commit -m "$SUBJECT"
fi

printf "\n✓ Commit successful.\n"

#!/bin/bash
# Supprime toute les données spécifique du projet memoviewer

echo "Reset all data from $memoviewer"

memoviewer=$1  # memoviewer main folder

rm -rfv $memoviewer/public/cards/*
rm -rfv $memoviewer/public/logo/*
rm -rfv $memoviewer/public/previews/*

rm -rfv $memoviewer/src/assets/icons/card-number-icon.svg
rm -rfv $memoviewer/src/assets/styles/local.scss
rm -rfv $memoviewer/src/components/about/*.vue
rm -rfv $memoviewer/src/data/*
rm -rfv $memoviewer/src/locales/*



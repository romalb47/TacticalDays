#!/bin/bash

cd ..
rm src/client/data/*
zip -r src/client/data/case.szip ressource/cases/
zip -r src/client/data/unité.ezip ressource/unités/
zip -r src/client/data/graphismes.szip ressource/graphismes/

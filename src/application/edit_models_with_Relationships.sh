vim `grep -wr "relationship" models | grep -vw "Binary file" | cut -f1 -d: | uniq`

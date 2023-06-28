find . -type f -name "*.sh" -exec sed -i 's/\r$//' {} +
find . -type f -name "*.sh" -exec chmod u+x {} +
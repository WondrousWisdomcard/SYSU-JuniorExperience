mkdir -p build
javac -encoding UTF-8 -d build -cp lib/jigsaw.jar src/solution/Solution.java
java -cp lib/jigsaw.jar:build judge.main
status=$?
if [ $status != 0 ]; then
    echo "Test Fail."
else
    echo "Test Pass."
fi

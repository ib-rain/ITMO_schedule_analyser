ERROR_MESSAGE="The script has failed, please start again."
GROUP_FILE="groups.txt"
ISU_FILE="isu_groups.txt"
LOAD_FILE="load.txt"
RES_FILE="result.csv"

: > $RES_FILE
: > $GROUP_FILE
: > $LOAD_FILE

echo "Performing 4-step schedule analysis..."

for i in $(seq 1 5)
do
    python get_groups.py $i >> $GROUP_FILE || {
        echo $ERROR_MESSAGE
        exit $((10+$i))
    }
done

echo "Done 1st."

python calc_isu.py $GROUP_FILE > $ISU_FILE || {
    echo $ERROR_MESSAGE
    exit 20
}

echo "Done 2nd."

for i in $(seq 1 5)
do
    python calc_load.py $ISU_FILE $i >> $LOAD_FILE || {
        echo $ERROR_MESSAGE
        exit $((30+$i))
    }
done

echo "Done 3rd."

python format_to_csv.py $LOAD_FILE $RES_FILE || {
    echo $ERROR_MESSAGE
    exit 40
}

echo "Finished."

# rm $GROUP_FILE $ISU_FILE $LOAD_FILE
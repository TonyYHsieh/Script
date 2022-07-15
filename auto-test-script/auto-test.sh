./clean.sh
rm -rf log/*

for alpha in 1 2
do
    for beta in 0 1
    do
        for ty in "h" "hh" "hb" "i8"
        do
            for tranA in "True" "False"
            do
                for tranB in "True" "False"
                do
                    cp header.yaml t.yaml
                    echo "  DataInitTypeAlpha: $alpha" >> t.yaml
                    echo "  DataInitTypeBeta: $beta" >> t.yaml
                    cat t.yaml middle.yaml > tt.yaml
                    if [ $ty == "h" ]
                    then
                        echo "      DataType: h" >> tt.yaml
                    elif [ $ty == "hh" ]
                    then
                        echo "      DataType: h" >> tt.yaml
                        echo "      HighPrecisionAccumulate: True" >> tt.yaml
                    elif [ $ty == "hb" ]
                    then
                        echo "      DataType: B" >> tt.yaml
                        echo "      DestDataType: B" >> tt.yaml
                        echo "      ComputeDataType: s" >> tt.yaml
                        echo "      HighPrecisionAccumulate: True" >> tt.yaml
                    elif [ $ty == "i8" ]
                    then
                        echo "      DataType: I8" >> tt.yaml
                        echo "      DestDataType: I" >> tt.yaml
                        echo "      HighPrecisionAccumulate: True" >> tt.yaml
                    fi
                    echo "      TransposeA: $tranA" >> tt.yaml
                    echo "      TransposeB: $tranB" >> tt.yaml
                    cat tt.yaml config.yaml > auto.yaml
                    ./run.sh auto.yaml
                    cp test.log log/$ty-$tranA-$tranB-$alpha-$beta.log
                    cp auto.yaml log/$ty-$tranA-$tranB-$alpha-$beta.yaml
                done
            done
        done
    done
done
echo "egrep FAIL"
egrep -srn FAIL log
echo "egrep success"
egrep -srn "clientExit=0" log | wc -l
echo "egrep fail"
egrep -srn "clientExit=1" log

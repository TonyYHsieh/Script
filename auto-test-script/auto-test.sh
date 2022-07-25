./clean.sh
rm -rf log/*

for alpha in 1 2
do
    for beta in 0 1
    do
#        for ty in "s" "c" "d" "z"
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
                    if [ $ty == "s" ]
                    then
                        echo "      DataType: s" >> tt.yaml
                    elif [ $ty == "d" ]
                    then
                        echo "      DataType: d" >> tt.yaml
                    elif [ $ty == "c" ]
                    then
                        echo "      DataType: c" >> tt.yaml
                    elif [ $ty == "z" ]
                    then
                        echo "      DataType: z" >> tt.yaml
                    elif [ $ty == "h" ]
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
echo "Total log"
ls -l log/*.log | wc -l
echo "num of success"
egrep -srn "clientExit=0" log | wc -l
echo "num of failure"
egrep -srn "clientExit=1" log | wc -l
echo "fail items"
egrep -srn "clientExit=1" log

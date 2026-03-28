@echo off
pip install requests pandas scikit-learn imbalanced-learn catboost
python download_and_train.py > train_log.txt 2>&1
echo Done > pipeline_done.txt

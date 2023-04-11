prefix=$(pwd)
cd $prefix/faas-share-test/MLPerf-based-workloads/resnet && sudo make download_pytorch_model

sudo mkdir /models/rnnt
sudo wget https://zenodo.org/record/3662521/files/DistributedDataParallel_1576581068.9962234-epoch-100.pt?download=1 -O /models/rnnt/rnnt.pt

sudo mkdir /models/bert
sudo wget 'https://api.ngc.nvidia.com/v2/models/nvidia/bert_pyt_ckpt_large_qa_squad11_amp/versions/19.09.0/files/bert_large_qa.pt' -O /models/bert/bert_large_qa.pt

sudo mkdir /models/gnmt
cd $prefix/faas-share-test/MLPerf-based-workloads/gnmt/model_exporter && sudo docker build -t gnmt_model_exporter . 
sudo docker run --rm --name gnmt-inst-exporter -v /models/gnmt:/models/gnmt gnmt_model_exporter

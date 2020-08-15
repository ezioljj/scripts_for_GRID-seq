name_list = ['C2C12.60h']

for element in name_list:
    element.strip("'")
    print "qsub" + " " + element + "." + "sh";
    file_name = element + ".sh"
    working_sh = open(file_name, 'w')
    s1 = "#PBS -N " + element + "\n"
    s2 = '''#PBS -l nodes=1:ppn=2
#PBS -l mem=10gb
#PBS -l walltime=7200:00:00
#PBS -q cu 

cd  $PBS_O_WORKDIR
##########'''
    s4 = "\n" + "sample=" + element + "\n"
    s3 = '''
if [ ! -d trim_real  ];then
mkdir trim_real
else
  echo "already exists"
fi

if [ ! -d trim_statistics  ];then
  mkdir trim_statistics
else
  echo "already exists"
fi

if [ ! -d final_output  ];then
  mkdir final_output
else
  echo "already exists"
fi

python3 001.contain_linker.py ${sample}_1.fq
python3 001.contain_linker.py ${sample}_2.fq

#for real extraction of DNA reads and RNA reads
trim_galore --stringency 1 --dont_gzip --length 79 --fastqc linker.${sample}_1.fq -o trim_real
trim_galore --stringency 1 --dont_gzip --length 79 --fastqc linker.${sample}_2.fq -o trim_real

cd trim_real
cat linker.${sample}_1_trimmed.fq linker.${sample}_2_trimmed.fq > ../${sample}.merged.fq
cd ..

python3 002.extract_reads.py ${sample}.merged.fq

#for statistics of reads length distribution
trim_galore --stringency 1 --dont_gzip --length 45 --fastqc linker.${sample}_1.fq -o trim_statistics
trim_galore --stringency 1 --dont_gzip --length 45 --fastqc linker.${sample}_2.fq -o trim_statistics

python3 004.extract_reads_for_statistics.py linker.${sample}_1_trimmed.fq
python3 004.extract_reads_for_statistics.py linker.${sample}_2_trimmed.fq

python3 003.statistics_reads.py DNA_reads.linker.${sample}_1_trimmed.fq
python3 003.statistics_reads.py DNA_reads.linker.${sample}_2_trimmed.fq
python3 003.statistics_reads.py RNA_reads.linker.${sample}_1_trimmed.fq
python3 003.statistics_reads.py RNA_reads.linker.${sample}_2_trimmed.fq
'''
    s = s1 + s2 + s4 + s3
    working_sh.write(s)


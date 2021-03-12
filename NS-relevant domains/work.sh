#python step01.prepare_speckle_mark_RNA.py

for i in 0h 60h
do
for j in rep1 rep2
do bedtools intersect -wa -wb -F 0.51 -a DNA.bin10k.bed -b speckle_marker.${j}.${i}.pkbin > 00.${j}.${i}.10kb.tmp
python step02.prepare_for_10kb.py 00.${j}.${i}.10kb.tmp 00.${j}.${i}.10kb
done
done

for i in 0h 60h
do
for j in rep1 rep2
do bedtools intersect -wa -wb -F 0.51 -a A_compartment.${i}.500kb -b 00.${j}.${i}.10kb > 01.${j}.${i}.A_interaction
done
done

for i in 0h 60h
do cat 01.rep1.${i}.A_interaction 01.rep2.${i}.A_interaction > 02.merged.${i}.A_interaction
done

#step03.search_for_cutoff.ipynb

python step03.prepare_zscore.py

for i in 0h 60h
do sort -k1,1 -k2,2n 04.speckle_${i}.bedgraph | bedtools merge -d 1000000 -i - > final_speckle_${i}.bed
done

awk '{OFS="\t"} $3-$2>=1000000 {print $0}' final_speckle_0h.bed > final_speckle_0h_larger.bed
awk '{OFS="\t"} $3-$2>=1000000 {print $0}' final_speckle_60h.bed > final_speckle_60h_larger.bed

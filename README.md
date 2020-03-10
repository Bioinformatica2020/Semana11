
## UNIVERSIDAD AUTÓNOMA METROPOLITANA, UNIDAD IZTAPALAPA

## HERRAMIENTAS BIOINFORMÁTICAS PARA LAS CIENCIAS BIOLÓGICAS: INTRODUCCIÓN A PYTHON
---
## ENSAMBLE DE GENOMA BACTERIANO
---

### [Ensambladores](http://www.metagenomics.wiki/tools/assembly)
### [Anotación](http://www.metagenomics.wiki/tools/annotation)

## PROCEDIMIENTO
- #### ANALISIS DE CALIDAD DE SECUENCIAS
- #### TRIMMING DE SECUENCIAS
- #### ALINEAMIENTO DE SECUENCIAS
- #### ENSAMBLE DE READS
- #### ANOTACIÓN ESTRUCTURAL USANDO Prokka
    * #### VISUALIZACIÓN DE LA ANOTACIÓN EN WINDOWS (`ARTEMIS`)
- #### ALINEAMIENTO DE READS A GENOMA ENSAMBLADO USANDO SAMTOOLS
    * #### EN TERMINAL LINUX
    * #### VISUALIZACIÓN DE LOS ALINEAMIENTOS EN WINDOWS (`IGV`)
- #### ANOTACIÓN FUNCIONAL DE GENES (GO Y KEGG)
- #### VISUALIZACIONES INTERACTIVAS EN UN AMBIENTE DE PYTHON
---

REQUERIMIENTOS (WINDOWS)

- INSTALACIÓN DE IGV
- INSTALACIÓN DE ARTEMIS
---

## 1. Ingresar al servidor desde la terminal

* ### Activar el entorno con los programas para el ensamblaje

```
    $ conda activate genome
```

## 2. Descomprimir todos los archivos .gz

```
    $ gunzip -d *.fastq.gz
```

## 3. Inspeccionar el archivo .fastq

```
    $ head SRR292770_1.fastq
```
## 4. Revisar la calidad de los reads con el programa [FASTQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

### Antes crear dos diretorios, uno por cada par de archivos

```
    $ mkdir 770

    $ mkdir 637
```

#### Revisar la calidad de los archivos `SRR292770_1.fastq`, `SRR292770_2.fastq`, `SRR396637_1.fastq` y `SRR396637_2.fastq`
[ENA Database](https://www.ebi.ac.uk/ena/browser/view/SRR292770)
```
    $ fastqc -o 770 SRR292770_1.fastq SRR292770_2.fastq

    $ fastqc -o 637 SRR396637_1.fastq SRR396637_2.fastq
``` 

* -o # directorio donde queremos guardar los resultados

## 5. Copiar archivos .html desde el servidor a mi ordenador

- Crear un directorio en mi ordenador donde guardaré los archivos que copie desde el servidor

- Esto se hace desde la terminal (Win + R) desde mi ordenador

```
    >scp -P 3030 curso■@148.206.50.100:/home/curso■/770/*.html .

    >scp -P 3030 curso■@148.206.50.100:/home/curso■/637/*.html .
```

* scp # comando de linux para copiar archivos o directorios  
* -P 3030 # puerto  
* curso■ # nombre del usuario en el servidor, ■ = 1-12  
* 148.206.50.100: # IP de acceso al servidor  
* /home/curso■/SRR292770_1.fastq # localización y nombre del archivo que se desea transferir desde el servidor  
* . # posicion en la que quiero depositar el archivo dentro de mi ordenador, en este caso me posicioné en un directorio específico  

## 6. Abrir cada uno de los archivos .html para explorar la calidad de los reads

* ### Usar un navegador para abrir los archivos .html

* ### Estimación de la cobertura del ensamblaje

```
    5102041 x 49 x 2 = 5e8 # número de bases

    5e8 / 4.6e6 = 100X # El genoma de E. coli en promedio mide 4.6Mb
```
* ### Se tiene una cobertura de 100, lo cual cubriría todo el genoma.

## 7. Trimming de secuencias (si es necesario) para eliminar bases/extremos de mala calidad

#### Se realizará trimming de secuencias únicamente en los archivos que presentan mala calidad, ya que estos presentan bases de mala calidad

* ### Primero descargar y descomprimir el programa [TrimGalore](https://github.com/FelixKrueger/TrimGalore/blob/master/Docs/Trim_Galore_User_Guide.md)

```
$ curl -fsSL https://github.com/FelixKrueger/TrimGalore/archive/0.6.5.tar.gz -o ./trimm/trim_galore.tar.gz

$ tar xvzf ./trimm/trim_galore.tar.gz
```

* ### Luego hacer trimming a las secuencias

```
     $ ./TrimGalore-0.6.5/trim_galore -o trimm --paired SRR396637_1.fastq SRR396637_2.fastq
```
#### Los archivos generados son `SRR396637_1_val_1.fq` y `SRR396637_2_val_2.fq`

* ### Ahora revisar la calidad de estos nuevos archivos

```
    $ mkdir 637_trimm

    $ fastqc -o 637_trimm ./trimm/SRR396637_1_val_1.fq ./trimm/SRR396637_2_val_2.fq
```
* ### Copiar los nuevos archivos .html desde el servidor a mi ordenador
```
    >scp -P 3030 curso■@148.206.50.100:/home/curso■/637_trimm/*.html .
```

## 8. Después de mejorar la calidad de las secuencias continuar con el ensamblaje usando los archivos `SRR292770_1.fastq` y `SRR292770_2.fastq`


# Ensamble con [VELVET](https://www.ebi.ac.uk/~zerbino/velvet/Manual.pdf) usando 29 k-mer

<img src="https://raw.githubusercontent.com/Bioinformatica2020/Semana11/master/covery.png" width = 70%>


## 9. `velveth`: construye nodos a partir de k-mers definidos

```
    $ velveth assem29 29 -fastq -shortPaired -separate SRR292770_1.fastq SRR292770_2.fastq
```

## 10. `velvetg`: es el core de Velvet, usa los nodos creados por velveth para construir los contigs

```
    $ velvetg assem29 -clean yes -exp_cov 21 -cov_cutoff 5 -min_contig_lgth 200
```
*  -exp_cov # cobertura esperada para un k-mer definido
* -cov_cutoff # umbral para remover nodos de baja cobertura

## 11. Contar el # de contigs obtenidos

grep ">" assem29/contigs.fa | wc -l

## 12.  Anotación estructural de Genoma usando [PROKKA](http://www.vicbioinformatics.com/software.prokka.shtml)
## creamos un nuevo directorio por cada prueba de k-mers

```
    $ prokka -setupdb

    $ prokka --outdir annotation assem29/contigs.fa
```
* ### Descargar el archivo `PROKKA_03102020.gbk` a mi ordenador
* ### Visualizar este archivo con el programa [ARTEMIS](https://www.sanger.ac.uk/science/tools/artemis)

## 13. Alineamiento de los reads a la secuencia ensamblada
 
* ### Descomprimir los arvhivos `bowtie2.sorted.bam.gz` y `bowtie2.sorted.bam.bai.gz`

```
    $ gunzip -c bowtie2.sorted.bam.gz > bowtie2.sorted.bam

    $ gunzip -c bowtie2.sorted.bam.bai.gz > bowtie2.sorted.bam.bai
```
* -c # Descomprime pero mantiene el archivo original

* ### Visualización en la terminal

```
    $ samtools tview bowtie2.sorted.bam assem29/contigs.fa
```
* ### Descargar los archivos `bowtie2.sorted.bam.gz` y `bowtie2.sorted.bam.bai.gz` a mi ordenador
* ### Visualizar estos archivos con el programa [IGV](https://software.broadinstitute.org/software/igv/AlignmentData)

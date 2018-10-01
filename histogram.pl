#!/usr/bin/perl

#########################################################
#							#
#   		          Histogram 	    		#
#							#
#	   	    D. Gonze  12/12/2003		#
#							#
#########################################################


### Variables globales:

my @data;
my $infile;
my $outfile;
my $col=1;
my $min="";
my $max="";
my $all=0;
my $int=1;
my $statsonly=0;
my $freq=0;
my $nx;


&ReadArguments;

open inf, $infile or die "STOP! File $infile not found";
if ($verbo==1) {print "Open input file: $infile\n";}
open ouf, ">$outfile";
if ($verbo==1) {print "Creating output file: $outfile\n";}

$col=$col-1;	# perl commence indice a 0

&CreateDataVector;

&Histo;

close inf;
close ouf;

if ($verbo==1) {print "It's finished\n";}


################################################################
### Read arguments from the command line

sub ReadArguments {

$ok=0;
$verbo=0;
$infile = "";
$outfile = "";
$xout="min";
$cumul=0;

foreach my $a (0..$#ARGV) {

    ### help
    if ($ARGV[0] eq "-h") {
    	&PrintHelp;
    }
            
    ### input file
    elsif ($ARGV[$a] eq "-i") {
	$ok = 1;
    	$infile = $ARGV[$a+1];
    }

    ### output file 
    elsif ($ARGV[$a] eq "-o") {
	$outfile = $ARGV[$a+1];
    }

    ### column with the data
    elsif ($ARGV[$a] eq "-col") {
    	$col = $ARGV[$a+1];
    }
	
    ### max
    elsif ($ARGV[$a] eq "-max") {
    	$max = $ARGV[$a+1];
    }

    ### min
    elsif ($ARGV[$a] eq "-min") {
    	$min = $ARGV[$a+1];
    }

    ### all
    elsif ($ARGV[$a] eq "-all") {
        $all = 1;
    }

    ### interval
    elsif ($ARGV[$a] eq "-int") {
    	$int = $ARGV[$a+1];
    }

    ### output stats only (suppress histogram bins)
    elsif ($ARGV[$a] eq "-stats-only") {
    	$statsonly = 1;
    }

    ### frequency
    elsif ($ARGV[$a] eq "-freq") {
    	$freq = 1;
    }

    ### x output
    elsif ($ARGV[$a] eq "-out") {
    	$xout = $ARGV[$a+1];
    }

    ### cumulative
    elsif ($ARGV[$a] eq "-cumul") {
    	$cumul = 1;
    }

    ### verbosity 
    elsif ($ARGV[$a] eq "-v") {
	$verbo = 1;
    }
	
}
	
if ($ok == 0) {
   die "STOP! You have to give the name of the input file!\n";
}
	
if ($outfile eq "") {
   $outfile = "$infile.histo";
}

} # End of Readargument


##########################################################################################
### Print help


sub PrintHelp {
  open HELP, "| more";
  print <<EndHelp;
NAME
        histogram.pl

DESCRIPTION
	Prepare data for histrogram.

AUTHOR
	Didier Gonze (dgonze\@ucmb.ulb.ac.be)  

UPDATED
	12/12/2003

OPTIONS
	-i in_file_name
		Specify the input file containing the data. 
		This argument is obligatory (except if using option -h).
	       
	-o out_file_name
		Specify the output file. Default name is in_file_name.histo

	-col #
		Specify the column containing the data. Default=1.

	-max #
		Specify the max for the histogram.
		Default: max of x-data.

	-min #
		Specify the min for the histogram.
		Default: min of x-data.
	
	-all
		If -max or -min are specified, bin all data outside of
		range in the extremum bins. For example, if "-min 10" is
		specified, bin all data < 10 in the first bin. Likewise
		for -max.

	-int #
		Specify the interval for the histogram. Default=1.
		
    -stats-only
        Output mean and standard deviation statistics only 
        and suppress histogram bins.

	-freq
		To have the frequency instead of the occurrence.
	
	-out [min,max,mean,minmax]
		To print the min, max, mean or both min and max for 
		each bin (x column). Default: min.
	
	-cumul
		To have the cumulative distribution (y columns).
		Warning: if the specified "min" (eith option -min) is
		greater than the real minimum of x-data, the cumulative
		distribution will not take account the data < min...
	
	-v 
		Verbosity: print detailed informations during the 
		process.
	       
	-h 
		Give help (print this message). This argument must be 
		the first.

REMARK
	If the x-data is on the border of a bin, it will be considered in the upper bin.
	(for ex: 5 will be counted in the interval [5,6] and not in [4,5]).
	NB: If all the data are real, you should use the option -out min (or default option)
	to have the exact correspondance between x-data and y-count.

EXAMPLE
        perl histogram.pl -i datafile -col 2 -max 10 -min 0 -int 1 -freq -o results.out

EndHelp
  close HELP;
die "\n";
}


##########################################################################################
### Read the data and fill the data vector

sub CreateDataVector {

my $i=0;
$dmin=99999999;
$dmax=-99999999;

$xsum=0;
foreach $line (<inf>){
   if ($line !~ /^#/ and $line ne ""){
      chomp $line;
      @line=split /\t| |,/,$line;      
      $x[$i]=$line[$col];
      
      if ($x[$i] <= $dmin) {$dmin=$x[$i]}
      elsif ($x[$i] >= $dmax) {$dmax=$x[$i]}
      
      $xsum=$xsum + $x[$i];
      $i=$i+1;
   }
}

if ($min eq ""){$min=$dmin;}    # automatic determination of min
if ($max eq ""){$max=$dmax;}    # automatic determination of max

$nx=$i;

##########################################################################################
### Stats
$xstdv_sum=0;
if ($nx > 0) {
    $xmean=$xsum/$nx;
}
else {
    $xmean=-1;
}

for ($i=0; $i <= $nx-1; $i++) {
  $xstdv_sum=$xstdv_sum + ( ($x[$i]-$xmean)**2 );
}

if ( $nx > 1 ) {
    $xstdv=( $xstdv_sum/($nx-1) )**(0.5);
}
else {
    $xstdv=-1;
}

$xmedn=&median(\@x);

if ($verbo==1) {print "Total number of data = $nx\n";}

} # End of CreateDataVector

##########################################################################################
### Histo

sub Histo {

my ($i,$j)=(0,0);
my $jmax;
my @z=0;

if ($verbo==1) {print "Generate data for histogram...\n";}

$jmax=($max-$min)/$int;

if ($statsonly==0) {
  for ($i=0; $i <= $nx-1; $i++) {
    for ($j=0; $j <= $jmax; $j++) {
      $cmin = $min + $j*$int;
      $cmax = $cmin + $int;
      if( ($x[$i] >= $cmin) and ($x[$i] < $cmax) ) {
        $z[$j] = $z[$j] + 1;
        #if ($verbo==1) {print "logic 1: $cmin <= $x[$i] < $cmax\n";}
        last;
      }
      elsif( ($all == 1) and ($x[$i] < $min) ) {
        $z[0] = $z[0] + 1;
        #if ($verbo==1) {print "logic 2: $x[$i] < $cmin\n";}
        last;
      }
      elsif( ($all == 1) and ($x[$i] >= $max)) {
        $z[$jmax] = $z[$jmax] + 1;
        #if ($verbo==1) {print "logic 3: $x[$i] >= $cmax\n";}
        last;
      }
    }
  }
}

$xmean_str=sprintf("%.6f",$xmean);
$xmedn_str=sprintf("%.6f",$xmedn);
$xstdv_str=sprintf("%.6f",$xstdv);
$nx_str=sprintf("%12d",$nx);
$xmin_str=sprintf("%.6f",$dmin);
$xmax_str=sprintf("%.6f",$dmax);
print ouf "Mean: $xmean_str\n";
print ouf "Medn: $xmedn_str\n";
print ouf "Stdv: $xstdv_str\n";
print ouf "Npts: $nx_str\n";
print ouf "Min : $xmin_str\n";
print ouf "Max : $xmax_str\n";

if ($statsonly==0) {
    print ouf "\nHistogram:\n";
}

  if ($statsonly==0) {
    for ($j=0;$j<=$jmax;$j++){
    
    $cmin=$min+$j*$int;
    $cmax=$cmin+$int;
    $cmean=($cmax+$cmin)/2;
    
    if ($freq==1) {$z[$j]=$z[$j]/$nx;}
     
    if($cumul==1 and $j>=1){
      $z[$j]=$z[$j]+$z[$j-1];
    }
    
    $zz=sprintf("%8d",$z[$j]);
    
    if ($xout eq "min") {print ouf "$cmin\t$zz\n";}
    elsif ($xout eq "max") {print ouf "$cmax\t$zz\n";}
    elsif ($xout eq "mean") {print ouf "$cmean\t$zz\n";}
    elsif ($xout eq "minmax") {print ouf "$cmin\t$cmax\t$zz\n";}
    else {$warn=1; print ouf "$cmin\t$zz\n";}
  }

}


if ($warn==1) {print "Warning: option $xout not defined! Output is min\n"}

} # End of Histo

sub median { 
    @_ == 1 or die ('Sub usage: $median = median(\@array);'); 
    my ($array_ref) = @_; 
    my $count = scalar @$array_ref; 
    
    # Sort a COPY of the array, leaving the original untouched 
    my @array = sort { $a <=> $b } @$array_ref; 
    if ($count % 2) { 
        return $array[int($count/2)]; 
    } else { 
        return ($array[$count/2] + $array[$count/2 - 1]) / 2; 
    } 
} 


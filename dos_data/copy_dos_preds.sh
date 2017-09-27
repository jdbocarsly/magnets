while read p; do
  cd $p
  scp jdb@braid.cnsi.ucsb.edu:/home/jdb/VASP/mcproxies_predictions/$p/dos/nonsp/dost.dat nonsp_dost.dat
  scp jdb@braid.cnsi.ucsb.edu:/home/jdb/VASP/mcproxies_predictions/$p/dos/sp/dost.dat sp_dost.dat
  cd /Users/Josh/Dropbox/proxy-flask/dos_data
done


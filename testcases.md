###Testing for Internet Archive import.  
#####    where fav-cateliper has already been imported into lbry.

1. Test without a source named.
    
>    python lbryimporter.py -a fav-cateliper
    
    Expected output:
        Please specify the type of import you want to run.
        A type of archive is required.
          use -h for help with more command line arguments

2. Test without a channel named, so publish via an anonymous channel, where published files already exist.
    
>    python lbryimporter.py -s internetarchive -a fav-cateliper
    
    Expected output:
        The file: TheBrideOfFrankensteinTrailer.mp4 -- already exists on the blockchain.
        Skipping the Publish.

3. Test Internet Archive w/o a collection name.
    
>    python lbryimporter.py -s internetarchive 
    
    Expected output:
       A collection name is required for importing Internet Archive content.
          use -h for help with more command line arguments
    
4. Test -h agruement
    
>    Expected output: Returns help info.
    
__The following tests will require using a collection, which hasn't previously been used to publish data__    
......    Otherwise the file publishing will be skipped

5. Publish a new file collection, where no --channel-name is provided, so it is anonymous
    
    Choose a channel name, which hasn't been imported previously.
    
>    python lbryimporter.py -s internetarchive -a SciFi_Horror
    
    Expected output:
       checking to see if the file <publish name> exists already in the blockchain.
       Successfully published the file

6. Publish a new file collection, where a --channel-name is provided.
    
    Choose a channel name, which hasn't been imported previously.
    
>    python lbryimporter.py -s internetarchive -a SciFi_Horror
    
    Expected output:
       checking to see if the file <publish name> exists already in the blockchain.
       Successfully published the file

    
    
__For the following tests, turn off Lbry app__

1. Test w/o LBRY app running.
    
>    python lbryimporter.py -s internetarchive -a fav-cateliper -c @internetarchive
    
    Expected output:
        'ERROR: The LBRY app or daemon must be running to import files into LBRY.' in log



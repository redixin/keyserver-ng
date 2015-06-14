
mkdir keys

for i in $(seq 1 4096); do

echo $i;
cat > keys/foo$i <<EOF
     %echo Generating a standard key
     Key-Type: DSA
     Key-Length: 1024
     Subkey-Type: ELG-E
     Subkey-Length: 1024
     Name-Real: Joe$i Tester
     Name-Comment: with stupid passphrase
     Name-Email: joe$i@foo.bar
     Expire-Date: 0
     Passphrase: abc$1
     %pubring foo.pub
     %secring foo.sec
     # Do a commit here, so that we can later print "done" :-)
     %commit
     %echo done
EOF
gpg --batch --gen-key keys/foo$i
gpg --no-default-keyring --secret-keyring ./keys/foo$i.sec \
    --keyring ./keys/foo$i.pub --list-secret-keys

done



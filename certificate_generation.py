# Import required modules
import subprocess

# Initialize global variables
h4="10.0.1.2"
keyName ="chatserver-key.pem"
csrName ="chatserver.csr"
certName ="chatserver-cert.pem"

# Get common name from user (Use tpa4.chat.test for chat server)
def getCmnName():
    cmnName=input("Enter the common name for your chat server (use 'tpa4.chat.test'): ")
    return cmnName

# Write common name to common_name.txt file
def writeCmnName(cmnName):
    with open("common_name.txt","w") as f:
        f.write(cmnName)

# Add host common name and IP address to /etc/hosts file
def addHost(cmnName):
    entry=h4+"\t"+cmnName
    # Read the etc/hosts file
    with open("/etc/hosts","rt") as in_f:
        lines=in_f.readlines()
    # Check if the entry already exists
    entry_exists = any(entry in line for line in lines)
    if entry_exists:
        print(f"The host entry for {cmnName} already exists in /etc/hosts.")
        return
    # Find the insert position at the end of IPv4 hosts list
    index=None
    for i, line in enumerate(lines):
        if "ip6-localhost" in line:
            index=i-1
            break
    # Insert the new host entry
    if index is not None:
        lines.insert(index,entry+"\n")
    # Write the updated content to a new temporary file
    with open("/tmp/tmp_hosts","wt") as out_f:
        out_f.writelines(lines)
    # Replace the original file with the updated file
    subprocess.run(["sudo","mv",'/tmp/tmp_hosts',"/etc/hosts"])

# Generate a new 2048 bit RSA private key for the server
def generatePrvKey():
    try:
        subprocess.run(["openssl","genrsa","-out",keyName,"2048"])
        print(f"Private key generated: {keyName}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating the private key: {e}")

# Generate a certificate signing request (CSR) for the server
def generateCSR(cmnName):
    subject = f"/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN={cmnName}"
    try:
        subprocess.run(["sudo","openssl","req","-nodes","-new","-config","/etc/ssl/openssl.cnf","-key",keyName,"-out",csrName,"-subj",subject])
        print(f"CSR generate: {csrName}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating the CSR: {e}")

# Generate the X.509 server certificate from the CSR
def generateCert():
    try:
        subprocess.run(["sudo","openssl","x509","-req","-days","365","-in",csrName,
                        "-CA","/etc/ssl/demoCA/cacert.pem","-CAkey","/etc/ssl/demoCA/private/cakey.pem",
                        "-CAcreateserial","-out",certName,"-passin","pass:Goldenwest1@"])
        print(f"Certificate generated: {certName}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating the certificate: {e}")


def main():
    # Prompt common name for chat server
        cmnName=getCmnName()
    # Write common name to a text file 
        writeCmnName(cmnName)
    # Add host common name and IP address to /etc/hosts file
        addHost(cmnName)
    # Generate private key
        generatePrvKey()
    # Generate a CSR for the server
        generateCSR(cmnName)
    # Generate the server certificate
        generateCert()

if __name__ == "__main__":
    main()
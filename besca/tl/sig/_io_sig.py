# this file contains the functions to read / import signatures
# for signature score computations
from re import match, compile
from requests import post


def read_GMT_sign(GMT_file, UP_suffix='_UP', DN_suffix='_DN', verbose=False):
    """ Read gmt file to extract signed genesets.
    This function combines genesets scores composed of
    UP and DN regulated genes.
    Non directional geneset are by default considered as UP.

    Parameters
    ----------
    GMT_file: `str` | default = None
        gmt file location containing the geneset
    UP_suffix : `str` | default = "_UP"
        str suffix indicating that the suffix indicating the signature is UP.
        This should be the end of the signatures names ($).
        Indicate a dummy string to avoid combination.
    DN_suffix : `str` | default = "_DN"
        str suffix indicating that the suffix indicating the signature is DN.
        This should be the end of the signatures names ($).
        Indicate a dummy string to avoid combination.
    Returns
    -------
    a dictionnary containing the signature names as key. \
    Value are a subdictionnary where key are direction(UP or DN).\
    Values are then the gene names.
    Example
    -------

    >>> #insert example code here
    >>> gmt_file= datasets/genesets/Immune.txt' # provided in besca
    >>> signature_dict = bc.tl.sig.read_GMT_sign(gmt_file)

    """
    signFile = open(GMT_file, "r")
    text_gmt = signFile.read().split('\n')
    signFile.close()
    signed_sign = {}
    # Here \S is used as signature might have '-' in their name
    #  (\w is not suficient if number in signature for EX.)
    pattern_DN = compile("(\S+)" + DN_suffix + "$")
    pattern_UP = compile("(\S+)" + UP_suffix + "$")
    # TODO: remove this for loop.
    for i in range(0, len(text_gmt)):
        temp_split = text_gmt[i].split('\t')
        signature_full_name = temp_split[0]
        if len(temp_split) < 3:
            if(verbose):
                print("Skipping empty entry" + signature_full_name)
            continue
        # Skipping empty lines in gmt files
        if len(signature_full_name):
            z = match(pattern_DN, signature_full_name)
            if(z):
                signatureName = z.groups()[0]
                direction = "DN"
            else:
                z = match(pattern_UP, signature_full_name)
                if(z):
                    signatureName = z.groups()[0]
                    direction = "UP"
                else:
                    signatureName = signature_full_name
                    direction = "UP"
            # Get the gene names removing empty entry
            initialValue = temp_split[2:len(temp_split)]
            geneArray = [x for x in initialValue if len(x)]
            if(signatureName in signed_sign.keys()):
                signed_sign[signatureName][direction] = geneArray
            else:
                signed_sign[signatureName] = {direction: geneArray}
            if (verbose):
                print(i, ": ", signature_full_name)
    return(signed_sign)



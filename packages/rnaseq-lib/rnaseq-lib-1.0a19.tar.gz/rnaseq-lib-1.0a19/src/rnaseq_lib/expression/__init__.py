from rnaseq_lib.gtf import dataframe_from_gtf


def calculate_tpm(df, gtf_path, output_dir='.'):
    """
    Calculate TPM given a dataframe of counts (genes by samples) and the corresponding GTF file



    :param pd.DataFrame df: Expression dataframe
    :param str gtf_path: Path to GTF file
    :param str output_dir: Output path of TPM TSV
    :return: TPM dataframe
    :rtype: pd.DataFrame
    """
    gtf = dataframe_from_gtf(gtf_path)

    tpms = {}


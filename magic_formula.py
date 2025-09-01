import pandas as pd

LIQUIDEZ_MEDIA_DIARIA_MINIMA = 1_000_000


def convert_number_comma_to_dot_in_csv(file_path: str) -> None:
    """
    Converte números com vírgula para ponto em um arquivo CSV.

    Args:
        file_path (str): Caminho do arquivo CSV de entrada.
    """
    df = pd.read_csv(file_path, dtype=str, sep=";")
    df = df.map(lambda x: x.replace(".", "") if isinstance(x, str) else x)
    df = df.map(lambda x: x.replace(",", ".") if isinstance(x, str) else x)
    df.to_csv("stocks_converted.csv", index=False)


def read_csv(file_path: str) -> pd.DataFrame:
    """
    Lê o arquivo csv, realiza conversões e filtragens

    Args:
        file_path (str): Caminho do arquivo CSV de entrada.

    Returns:
        pd.DataFrame: DataFrame contendo os dados filtrados e convertidos.
    """
    df = pd.read_csv(file_path, sep=",")
    df["P/L"] = pd.to_numeric(df["P/L"], errors="coerce")
    df["ROE"] = pd.to_numeric(df["ROE"], errors="coerce")
    df["EV/EBIT"] = pd.to_numeric(df["EV/EBIT"], errors="coerce")
    df["ROIC"] = pd.to_numeric(df["ROIC"], errors="coerce")
    df[" LIQUIDEZ MEDIA DIARIA"] = pd.to_numeric(df[" LIQUIDEZ MEDIA DIARIA"], errors="coerce")
    df = df[df[" LIQUIDEZ MEDIA DIARIA"] > LIQUIDEZ_MEDIA_DIARIA_MINIMA]
    return df


def magic_formula_pl_roe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica a fórmula mágica de Greenblatt usando P/L e ROE.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados das ações.

    Returns:
        pd.DataFrame: DataFrame contendo os resultados da fórmula mágica.
    """
    df = df[df["P/L"] > 0]
    df_pl = df.sort_values(by="P/L").reset_index(drop=True)
    df_pl["RANK_P/L"] = df_pl.index + 1
    df_roe = df.sort_values(by="ROE", ascending=False).reset_index(drop=True)
    df_roe["RANK_ROE"] = df_roe.index + 1
    df_pl = df_pl[["TICKER", "RANK_P/L"]]
    df_final = pd.merge(df_pl, df_roe, on=["TICKER"])
    df_final["RANK_FINAL"] = df_final["RANK_P/L"] + df_final["RANK_ROE"]
    list_of_fields = ["TICKER", "RANK_P/L", "RANK_ROE", "RANK_FINAL", "PRECO", "P/L", "ROE", " LIQUIDEZ MEDIA DIARIA"]
    cols = list_of_fields + [col for col in df_final.columns if col not in list_of_fields]
    df_final = df_final[cols]
    df_final = df_final.sort_values(by="RANK_FINAL").reset_index(drop=True)
    return df_final


def magic_formula_ev_ebit_roic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica a fórmula mágica de Greenblatt usando EV/EBIT e ROIC.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados das ações.

    Returns:
        pd.DataFrame: DataFrame contendo os resultados da fórmula mágica.
    """
    df = df[df["EV/EBIT"] > 0]
    df_ev_ebit = df.sort_values(by="EV/EBIT").reset_index(drop=True)
    df_ev_ebit["RANK_EV/EBIT"] = df_ev_ebit.index + 1
    df_roic = df.sort_values(by="ROIC", ascending=False).reset_index(drop=True)
    df_roic["RANK_ROIC"] = df_roic.index + 1
    df_ev_ebit = df_ev_ebit[["TICKER", "RANK_EV/EBIT"]]
    df_final = pd.merge(df_ev_ebit, df_roic, on=["TICKER"])
    df_final["RANK_FINAL"] = df_final["RANK_EV/EBIT"] + df_final["RANK_ROIC"]
    list_of_fields = [
        "TICKER",
        "RANK_EV/EBIT",
        "RANK_ROIC",
        "RANK_FINAL",
        "PRECO",
        "EV/EBIT",
        "ROIC",
        " LIQUIDEZ MEDIA DIARIA",
    ]
    cols = list_of_fields + [col for col in df_final.columns if col not in list_of_fields]
    df_final = df_final[cols]
    df_final = df_final.sort_values(by="RANK_FINAL").reset_index(drop=True)
    return df_final


def export_results_to_excel(df_final: pd.DataFrame, file_path: str):
    """
    Exporta os resultados para um arquivo Excel.

    Args:
        df_final (pd.DataFrame): DataFrame contendo os resultados da fórmula mágica.
        file_path (str): Caminho do arquivo Excel de saída.
    """
    df_final.to_excel(file_path, index=False)


if __name__ == "__main__":
    convert_number_comma_to_dot_in_csv("stocks.csv")
    df = read_csv("stocks_converted.csv")
    df_final_pl_roe = magic_formula_pl_roe(df)
    export_results_to_excel(df_final_pl_roe, "magic_formula_results_pl_roe.xlsx")
    df_final_ev_ebit_roic = magic_formula_ev_ebit_roic(df)
    export_results_to_excel(df_final_ev_ebit_roic, "magic_formula_results_ev_ebit_roic.xlsx")

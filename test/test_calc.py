import pytest
import nzfiftax as fif


def test_import_sharsies_csv():
    test_file_path = './resources/test_transactions.csv'
    df = fif.import_sharesies_csv(test_file_path)
    known_rows = 49
    assert df.shape[0] == known_rows


@pytest.fixture
def test_data1():
    test_file_path = './resources/test_transactions.csv'
    df = fif.import_sharesies_csv(test_file_path)
    return df


def test_peak_holding_differential(test_data1):
    expected_peak_hd = 0
    peak_hd = fif.peak_holding_differential(test_data1, ticker='YOLO')
    assert peak_hd == expected_peak_hd

    expected_peak_hd = 133
    peak_hd = fif.peak_holding_differential(test_data1, ticker='FUEL')
    assert peak_hd == expected_peak_hd

    expected_peak_hd = 136.02751144
    peak_hd = fif.peak_holding_differential(test_data1, ticker='TECH')
    assert peak_hd == expected_peak_hd


def test_average_cost_nzd(test_data1):
    expected_avg_cost = 38.952
    avg_cost = fif.average_cost_nzd(test_data1, ticker='YOLO')
    assert avg_cost == pytest.approx(expected_avg_cost, rel=1e-3)

    expected_avg_cost = 87.890
    avg_cost = fif.average_cost_nzd(test_data1, ticker='FUEL')
    assert avg_cost == pytest.approx(expected_avg_cost, rel=1e-3)

    expected_avg_cost = 504.61
    avg_cost = fif.average_cost_nzd(test_data1, ticker='TECH')
    assert avg_cost == pytest.approx(expected_avg_cost, rel=1e-3)


def test_peak_holding_method(test_data1):
    expected_phm_val = 0
    phm_val = fif.peak_holding_method(test_data1, 'YOLO')
    assert phm_val == pytest.approx(expected_phm_val, rel=1e-3)

    expected_phm_val = 584.47
    phm_val = fif.peak_holding_method(test_data1, 'FUEL')
    assert phm_val == pytest.approx(expected_phm_val, rel=1e-3)

    expected_phm_val = 3432.04
    phm_val = fif.peak_holding_method(test_data1, 'TECH')
    assert phm_val == pytest.approx(expected_phm_val, rel=1e-3)


def test_taxable_amount(test_data1):
    expected_amount = 0
    taxable_amount = fif.taxable_amount(test_data1, 'YOLO')
    assert taxable_amount == pytest.approx(expected_amount, rel=1e-3)

    expected_amount = 584.47
    taxable_amount = fif.taxable_amount(test_data1, 'FUEL')
    assert taxable_amount == pytest.approx(expected_amount, rel=1e-3)

    expected_amount = 867.6
    taxable_amount = fif.taxable_amount(test_data1, 'TECH')
    assert taxable_amount == pytest.approx(expected_amount, rel=1e-3)


def test_list_tickers(test_data1):
    expected_tickers = ['YOLO', 'FUEL', 'TECH']
    tickers = fif.list_tickers(test_data1)
    assert tickers == expected_tickers


def test_gain_method(test_data1):
    expected_gain = 578.46
    gain = fif.gain_method(test_data1, 'YOLO')
    assert gain == pytest.approx(expected_gain, rel=1e-3)

    expected_gain = 1203.10
    gain = fif.gain_method(test_data1, 'FUEL')
    assert gain == pytest.approx(expected_gain, rel=1e-3)

    expected_gain = 867.62
    gain = fif.gain_method(test_data1, 'TECH')
    assert gain == pytest.approx(expected_gain, rel=1e-3)


def test_filter_by_ticker(test_data1):
    df = fif.filter_by_ticker(test_data1, 'YOLO')
    for dix, r in df.iterrows():
        assert r['Instrument code'] == 'YOLO'




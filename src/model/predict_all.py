def predict_all(df):
    import pandas as pd

    from universal_predictor import predict

    df = pd.concat([df, predict(df, "model_for_speed", "speed")], axis=1)
    print('speed_predicted')
    df = pd.concat([df, predict(df, "model_for_load", "load")], axis=1)
    print('load_predicted')
    df = pd.concat([df, predict(df, "model_for_point", "point")], axis=1)
    print('point_predicted')
    df = pd.concat([df, predict(df, "model_for_amount", "amount")], axis=1)
    print('amount_predicted')
    return df
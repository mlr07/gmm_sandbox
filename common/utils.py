def verbose_info(log_data:dict):
    for k,v in log_data.items():
        if not isinstance(v, str):
            print(f"{k}: {type(v)}")
        else:
            print(f"{k}: {v}")

    print("-"*50)

    print(f"base df: {log_data['base_curves'].shape}")
    print(f"scaled curves:{log_data['scaled_curves'].shape}")
    print(f"pca arr: {log_data['pca_curves'].shape}")
    print(f"pca expvar: {log_data['pca_curves'].shape}")
    print(f"pca rank: {log_data['pca_rank'].shape}")
    print(f"soft arr: {log_data['soft_clusters'].shape}")
    print(f"hard arr: {log_data['hard_clusters'].shape}")
    print(f"merged df: {log_data['merged_curves'].shape}")
    print(f"merged pca: {log_data['merged_pca'].shape}")
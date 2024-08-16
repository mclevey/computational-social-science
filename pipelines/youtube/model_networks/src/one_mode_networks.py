import pickle

import graph_tool.all as gt
import pandas as pd
import yaml

import icsspy
import icsspy.networks as networks

logger = icsspy.initialize_logger()


with open("model_networks.yaml", "r") as file:
    task_config = yaml.safe_load(file)

channel_networks = task_config.get("one_mode_channel_networks")

all_ppm_bd, all_hbsbm_bd = [], []
for netname, netpath in channel_networks.items():
    g = networks.load_gt(netpath)
    if g.num_vertices() > 0 and g.num_edges() > 0:
        # FIT A FLAT BAYESIAN PLANTED PARTITION MODEL #
        blockstate_ppm, block_data_ppm = networks.fit_bppm(g, refine="basic")

        block_data_ppm["netname"] = netname

        # draw the blockmodel
        blockstate_ppm.draw(
            vprops={
                "text": g.vp["vprop_name"],
                "text_position": 0,
                "text_color": "black",
                "size": 30,
                "font_size": 12,
                # "fill_color": blockstate_ppm.get_blocks(),
            },
            output=f"../output/{netname}_ppm.pdf",
            output_size=(3000, 3000),
            bg_color=[1, 1, 1, 1],
            inline=True,
        )

        # write blockstate and blockdata to disk
        all_ppm_bd.append(block_data_ppm)

        with open(f"../output/{netname}_ppm_blockstate.pkl", "wb") as f:
            pickle.dump(blockstate_ppm, f)

        logger.info(f"Estimated a Bayesian PPM for {netname}\n")

        # FIT A HIERARCHICAL BAYESIAN STOCHASTIC BLOCKMODEL #
        blockstate_hbsbm, block_data_hbsbm = networks.fit_hbsbm(
            g, refine="basic", return_all_levels=True
        )

        block_data_hbsbm["netname"] = netname

        # draw the blockmodel
        gt.draw_hierarchy(
            blockstate_hbsbm,
            output=f"../output/{netname}_hbsbm.pdf",
            output_size=(3000, 3000),
            bg_color=[1, 1, 1, 1],
            vprops={
                "text": g.vp["vprop_name"],
                "text_position": 0,
                "text_color": "black",
            },
        )

        # write blockstate and blockdata to disk
        all_hbsbm_bd.append(block_data_hbsbm)

        with open(f"../output/{netname}_hbsbm_blockstate.pkl", "wb") as f:
            pickle.dump(blockstate_ppm, f)

        logger.info(f"Estimated a Hierarchical Bayesian SBM for {netname}\n")


all_ppm_bd = pd.concat(all_ppm_bd)
all_ppm_bd.to_csv(
    f"../output/{netname}_entity_entity_all_block_data_ppm.csv", index=False
)

all_hbsbm_bd = pd.concat(all_hbsbm_bd)
all_hbsbm_bd.to_csv(
    f"../output/{netname}_entity_entity_all_block_data_hbsbm.csv", index=False
)

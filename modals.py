# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 23:35:56 2020

@author: joeda
"""


from flask_babel import _ ,Babel

import dash_core_components as dcc
import dash_html_components as html

def build_modal_info_overlay(id, side, content):
    """
    Build div representing the info overlay for a plot panel
    """
    div = html.Div(
        [  # modal div
            html.Div(
                [  # content div
                    html.Div(
                        [
                            html.H4(
                                [
                                    "Info",
                                    html.Img(
                                        id=f"close-{id}-modal",
                                        src="assets/times-circle-solid.svg",
                                        n_clicks=0,
                                        className="info-icon",
                                        style={"margin": 0},
                                    ),
                                ],
                                className="container_title",
                                style={"color": "white"},
                            ),
                            dcc.Markdown(content),
                        ]
                    )
                ],
                className=f"modal-content {side}",
            ),
            html.Div(className="modal"),
        ],
        id=f"{id}-modal",
        style={"display": "none"},
    )

    return div


def modals_language() :

        modals=html.Div(children=[
                        build_modal_info_overlay(
                            "model",
                            "bottom",
                           _(

                    "This dropdown menu allows for the selection of  a model to generate the space in which walker \
                    will be set free. This model can take the form of a simple cartesian grid or can be made from \
                    a more complex model, for example a small-world network"

                            ),
                        ),
                        build_modal_info_overlay(
                            "connectivity",
                            "bottom",
                            _(

                    "This parameter controls the number of connection associated to each node. It has been normalize on a scale from 1 to 10, \
                    with the formula C=N/100*connectivity. By default those connection are made between neighboring nodes."

                            ),
                        ),
                        build_modal_info_overlay(
                            "connectivity_node",
                            "bottom",
                            _("This parameter  represent the probability of randomly reasigning the end connection between two nodes, scaled from 1 to 10. This allows the formation  \
                              of a randomly organized network of type small-world. If this factor is set at 10, the graph will be completely random.")
                            ),

                        build_modal_info_overlay(
                            "size",
                            "top",
                            _("This parameters simply control the raw size of the network in nodes. For example, on \
                    a cartesian grid going from x=[-5,5],y=[-5,5], the dimension would be a 100 nodes.")

                        ),

                         build_modal_info_overlay(
                            "n_walker",
                            "top",
                            _("The number of walkers(people) roaming the network. This parameter should not be set too low \
                    in order for the result to have any statistical significance. This parameter will also affect \
                    the 'population density', given by n_walkers/size, which will be one of the main factor that will \
                    determine the outcome of the epidemic."

                            )
                        ),

                          build_modal_info_overlay(
                            "n_repetition",
                            "top",
                            _(


                    "This allows the simulation to be repeated multiple times in order to \
                    estimate a standard deviation on the result. The error bars are generated \
                    as 0.2 times the standard deviation."

                            ),
                        ),


                           build_modal_info_overlay(
                            "preset",
                            "top",
                            _(

                    "The Signal Range panel displays a histogram of the signal range of \
                    each tower in the dataset.  The dark gray bars represent the set of towers \
                    in the current selection, while the light gray bars underneath represent \
                    all towers in the dataset."


                            ),
                        ),

                             build_modal_info_overlay(
                            "mortality",
                            "top",
                            _(

                    "The probability a person has to die once the lifetime of the disease has come to an \
                    end. We assume those who survive cannot get infected back. For technical reason, it is \
                    scaled from 1 to 10 instead of 0 to 1."

                            ),
                        ),

                            build_modal_info_overlay(
                            "infectiosity",
                            "top",
                            _(
                                " \
                    The probability of a person getting infected when passing by a node with another infected person on it.\
                    For technical reason, it is scaled from 1 to 10 instead of 0 to 1."

                            ),
                        ),

                             build_modal_info_overlay(
                            "n_sick",
                            "top",
                            _("The number of sick person at the first iteration. For a small population density, this could affect greatly the outcome. However, \
                    for a bigger population density, this parameter should not affect too much the outcome of the epidemic."

                            ),
                        ),

                                build_modal_info_overlay(
                            "duree",
                            "top",
                            _("The lifetime of the disease. Once a person is infected, it will remain contagious until \
                    his lifetime is over, and it will then either recover (and be immune to the disease) or die."
                            ),
                        ),
                        build_modal_info_overlay(
                            "created",
                            "top",
                            _(

                    "The Construction Date panel displays a histogram of the construction \
                    date of each tower in the dataset.  The dark gray bars represent the set of \
                    towers in the current selection, while the light gray bars underneath \
                    represent all towers in the dataset. "

                            ),
                        )])


        return modals

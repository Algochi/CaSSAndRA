from dash import html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc

from .. import ids
from . import buttons
from src.backend.data import saveddata
from src.backend.data.mapdata import current_map, mapping_maps, current_task
from src.backend.data.roverdata import robot

sunrayimportstatus = dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle(id=ids.MODALSUNRAYIMPORTTITLE)),
                            dbc.ModalBody(id=ids.MODALSUNRAYIMPORTBODY),
                            dbc.ModalFooter([
                                buttons.okbuttonsunrayimport,  
                            ] ),
                        ],
                        id=ids.MODALSUNRAYIMPORT,
                        is_open=False,
                    )

overwriteperimter = dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle('Info')),
                            dbc.ModalBody('Please give an unique name for new perimeter'),
                            dbc.ModalBody(dbc.Input(id=ids.INPUTPERIMETERNAME, type='text')),
                            dbc.ModalFooter([
                                buttons.okbuttonoverwriteperimter,  
                            ] ),
                        ],
                        id=ids.MODALOVERWRITEPERIMETER,
                        is_open=False,
                    )

newperimeter = dbc.Modal([
                            dbc.ModalHeader(dbc.ModalTitle('Info')),
                            dbc.ModalBody('Create new perimeter from scratch?'),
                            dbc.ModalFooter([
                                buttons.okbuttonnewperimeter,  
                            ] ),
                        ],
                        id=ids.MODALADDNEWPERIMETER,
                        is_open=False,          
                )

selectperimeter = dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle('Info')),
                        dbc.ModalBody('Continue with selected perimeter'),
                        dbc.ModalFooter([
                            buttons.okbuttonselectedperimeter,  
                            ] 
                        ),
                    ],
                    id=ids.MODALSELECTEDPERIMETER,
                    is_open=False,          
                )

copyperimeter = dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle('Info')),
                        dbc.ModalBody('Copy perimeter?'),
                        dbc.ModalBody(dbc.Input(id=ids.INPUTCOPYPERIMETER,placeholder='Please give an unique name', type='text')),
                        dbc.ModalFooter([
                            buttons.okbuttoncopyperimeter,  
                            ] 
                        ),
                    ],
                    id=ids.MODALCOPYPERIMETER,
                    is_open=False,          
                )

removeperimeter = dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle('Warning')),
                        dbc.ModalBody('Remove selected perimeter?'),
                        dbc.ModalFooter([
                            buttons.okbuttonremoveperimeter,  
                            ] 
                        ),
                    ],
                    id=ids.MODALREMOVEPERIMETER,
                    is_open=False,          
                )

finishmapping = dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle('Info')),
                        dbc.ModalBody('Finish mapping? Please give an unique name'),
                        dbc.ModalBody(dbc.Input(id=ids.INPUTNEWPERIMETERNAME, type='text')),
                        dbc.ModalFooter([
                            buttons.okbuttonfinishmapping,  
                            ] 
                        ),
                    ],
                    id=ids.MODALFINISHMAPPING,
                    is_open=False,          
                )

nofixsolution = dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle('Warning')),
                        dbc.ModalBody('No fix solution available! Continue anyway?'),
                        dbc.ModalFooter([
                            buttons.okbuttonnofixsolution,  
                            ] 
                        ),
                    ],
                    id=ids.MODALNOFIXSOLUTION,
                    is_open=False,          
                )

@callback(Output(ids.MODALOVERWRITEPERIMETER, 'is_open'),
          [Input(ids.BUTTONSAVEIMPORTEDPERIMETER, 'n_clicks'),
           Input(ids.OKBUTTONOVERWRITEPERIMTER, 'n_clicks'),
           State(ids.DROPDOWNSUNRAYIMPORT, 'value'),
           State(ids.MODALOVERWRITEPERIMETER, 'is_open'),
           State(ids.INPUTPERIMETERNAME, 'value')])
def overwrite_perimeter(bsp_n_clicks: int, bok_n_clicks, map_nr: str(), 
                        is_open: bool, perimeter_name: str()) -> bool:
    context = ctx.triggered_id
    if context == ids.OKBUTTONOVERWRITEPERIMTER:
        mapping_maps.select_imported(map_nr)
        if mapping_maps.select_imported_status == 0:
            saveddata.save_perimeter(mapping_maps.saved, mapping_maps.selected_import, perimeter_name)
    if bsp_n_clicks or bok_n_clicks:
        return not is_open
    return is_open

@callback(Output(ids.MODALSELECTEDPERIMETER, 'is_open'),
          [Input(ids.BUTTONSELECTPERIMETER, 'n_clicks'),
           Input(ids.OKBUTTONSELECTEDPERIMETER, 'n_clicks'),
           State(ids.DROPDOWNCHOOSEPERIMETER, 'value'),
           State(ids.MODALSELECTEDPERIMETER, 'is_open'),])
def selected_perimeter(bsp_n_clicks: int, bok_n_clicks: int, 
                       selected_perimeter: str(), is_open: bool) -> list:
    context = ctx.triggered_id
    if selected_perimeter == None:
        return is_open
    selected = mapping_maps.saved[mapping_maps.saved['name'] == selected_perimeter] 
    if context == ids.OKBUTTONSELECTEDPERIMETER:
        current_map.perimeter = selected
        current_map.create(selected_perimeter)
        current_task.create()
    if bsp_n_clicks or bok_n_clicks:
        return not is_open
    return is_open

@callback(Output(ids.MODALADDNEWPERIMETER, 'is_open'),
          [Input(ids.BUTTONADDNEWPERIMETER, 'n_clicks'),
           Input(ids.OKBUTTONNEWPERIMETER, 'n_clicks'),
           State(ids.MODALADDNEWPERIMETER, 'is_open')])
def new_perimeter(baddp_n_clicks: int, bok_n_clicks, is_open: bool) -> bool:
    if baddp_n_clicks or bok_n_clicks:
        return not is_open
    return is_open

@callback(Output(ids.MODALCOPYPERIMETER, 'is_open'),
          [Input(ids.BUTTONCOPYPERIMETER, 'n_clicks'),
           Input(ids.OKBUTTONCOPYPERIMETER, 'n_clicks'),
           State(ids.INPUTCOPYPERIMETER, 'value'),
           State(ids.DROPDOWNCHOOSEPERIMETER, 'value'),
           State(ids.MODALCOPYPERIMETER, 'is_open')])
def copy_perimeter(bcp_n_clicks: int, bok_n_clicks: int, 
                     cpy_perimeter_name: str(), selected_perimeter: str(),
                     is_open: bool) -> bool:
    context = ctx.triggered_id
    if context == ids.OKBUTTONCOPYPERIMETER:
        saveddata.copy_perimeter(mapping_maps.saved, selected_perimeter, cpy_perimeter_name)
    if bcp_n_clicks or bok_n_clicks:
        return not is_open
    return is_open

@callback(Output(ids.MODALREMOVEPERIMETER, 'is_open'),
          [Input(ids.BUTTONREMOVEPERIMETER, 'n_clicks'),
           Input(ids.OKBUTTONREMOVEPERIMETER, 'n_clicks'),
           State(ids.DROPDOWNCHOOSEPERIMETER, 'value'),
           State(ids.MODALREMOVEPERIMETER, 'is_open')])
def remove_perimeter(brp_n_clicks: int, bok_n_clicks, 
                     selected_perimeter: str(), is_open: bool) -> bool:
    context = ctx.triggered_id
    if context == ids.OKBUTTONREMOVEPERIMETER:
        saveddata.remove_perimeter(mapping_maps.saved, selected_perimeter)
    if brp_n_clicks or bok_n_clicks:
        return not is_open
    return is_open

@callback(Output(ids.MODALFINISHMAPPING, 'is_open'),
          [Input(ids.BUTTONFINISHFIGURE, 'n_clicks'),
           Input(ids.OKBUTTONFINISHMAPPING, 'n_clicks'),
           State(ids.INPUTNEWPERIMETERNAME, 'value'),
           State(ids.MODALFINISHMAPPING, 'is_open')])
def finish_mapping(bff_n_clicks: int, bok_n_clicks: int, 
                   perimeter_name: str(), is_open: bool) -> bool:
    context = ctx.triggered_id
    if context == ids.OKBUTTONFINISHMAPPING:
        mapping_maps.check_dockpoints()
        saveddata.save_perimeter(mapping_maps.saved, mapping_maps.build, perimeter_name)
    if bff_n_clicks or bok_n_clicks:
        return not is_open
    return is_open

@callback(Output(ids.MODALNOFIXSOLUTION, 'is_open'),
          [Input(ids.BUTTONADDNEWPOINT, 'n_clicks'),
           Input(ids.OKBUTTONNOFIXSOLUTION, 'n_clicks'),
           State(ids.BUTTONHOMEADD, 'n_clicks'),
           State(ids.MODALNOFIXSOLUTION, 'is_open')])
def nofix_solution(banp_n_clicks: int, bok_n_clicks, bha_state: bool,
                   is_open: bool) -> bool:
    context = ctx.triggered_id
    if bha_state:
        create = 'dockpoints'
    else:
        create = 'figure'
    if context == ids.BUTTONADDNEWPOINT and robot.position_solution == 2:
        mapping_maps.add_point(create)
        return is_open
    elif context == ids.BUTTONADDNEWPOINT and robot.position_solution != 2:
        return not is_open
    elif context == ids.OKBUTTONNOFIXSOLUTION:
        mapping_maps.add_point(create)
    else:
        return is_open
   
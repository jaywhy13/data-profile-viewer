import React from 'react';
import axios from 'axios';


class ColumnRow extends React.Component {

    state = {};

    constructor() {
        super();
        this.updateHasDuplicates = this.updateHasDuplicates.bind(this);
        this.updateIsStructured = this.updateIsStructured.bind(this);
        this.updateNeedsIndex = this.updateNeedsIndex.bind(this);
    }

    componentDidMount () {
        this.setState(Object.assign({}, this.props.column, {}));
    }

    updateIsStructured() {
        console.log("Updating is structured");
        axios.post(`/api/column/${this.state.id}/update_is_structured/`,
                {is_structured: !this.state.is_structured}).then((response) => {
            this.setState({is_structured: response.data.is_structured})
        });
    }

    updateHasDuplicates() {
        axios.post(`/api/column/${this.state.id}/update_has_duplicates/`,
                {has_duplicates: !this.state.has_duplicates}).then((response) => {
            this.setState({has_duplicates: response.data.has_duplicates})
        });
    }

    updateNeedsIndex() {
        axios.post(`/api/column/${this.state.id}/update_needs_index/`,
                {needs_index: !this.state.needs_index}).then((response) => {
            this.setState({needs_index: response.data.needs_index})
        });
    }

    render () {
        return (
            <tr>
                <td>
                    <span className="column-name">{this.state.name}</span>
                    <span 
                        className="column-data-type">({this.state.data_type})</span>
                    <span 
                        className="column-nullable">
                            {this.state.is_null ? "nullable" : ""}
                    </span>
                </td>
                <td>
                    {(this.state.minimum || this.state.maximum) ? this.state.minimum + " / " + this.state.maximum : "" }
                </td>
                <td>
                    {this.state.standard_deviation}
                </td>
                <td>
                    {this.state.max_length}
                </td>
                <td>
                    {Math.round(this.state.null_count) ? Math.round(this.state.null_count) : "" }
                    {Math.round(this.state.null_count) ? "(" + (this.state.percentage_of_nulls * 100) + "%)" : "" }
                </td>
                <td>
                    <a href="javascript:void(0)" onClick={() => this.props.onColumnUniqueValueClicked(this.state.id)}>
                        {this.state.unique_values}
                    </a>
                </td>
                <td>
                    <input 
                        type="checkbox" checked={this.state.has_duplicates} 
                        onChange={this.updateHasDuplicates}
                    />
                </td>
                <td>
                    <input 
                        type="checkbox" checked={this.state.is_structured} 
                        onChange={this.updateIsStructured}
                    />
                </td>
                <td>
                    <input 
                        type="checkbox" checked={this.state.needs_index} 
                        onChange={this.updateNeedsIndex}
                    />
                </td>
            </tr>
        );
    }

}

export default ColumnRow;
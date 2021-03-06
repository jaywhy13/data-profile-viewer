import React from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ReactPaginate from 'react-paginate';
import './TableList.css';


class TableList extends React.Component {

    state = {
        tables: [],
        limit: 30,
        offset: 0,
        total: 0,
        numberOfPages: 0,
        query: "",
    }

    constructor() {
        super();
        this.handleSearch = this.handleSearch.bind(this);
    }

    componentDidMount(){
        console.log("Fetching tables");
        this.loadTables();
    }

    pageChanged(page) {
        this.setState({
            'offset': page * 30,
        }, () => {
            this.loadTables();
        })
    }

    loadTables() {
        axios.get(`/api/table/?offset=${this.state.offset}&limit=${this.state.limit}&q=${this.state.query}`).then((response) => {
            console.log("Got back response: ", response.data);
            this.setState({
                'tables': response.data.results,
                'total': response.count,
                'numberOfPages': Math.round(response.data.count / 30)
            })
        });
    }

    updateUseForBi (table) {
        axios.post(`/api/table/${table.name}/update_use_for_bi/`, {use_for_bi: !table.use_for_bi}).then((response) => {
            let updatedTables = this.state.tables.map((table_) => {
                if(table_.name === table.name){
                    table_.use_for_bi = !table.use_for_bi;
                }
                return table_;
            });
            this.setState({tables: updatedTables});
        });
    }

    handleSearch(event) {
        this.setState({query: event.target.value}, () => {
            this.loadTables();
        })
    }

    render () {
        var rows = this.state.tables.map((table) => {
            return (
                <tr key={table.id}>
                    <td>
                        <Link to={table.name}>{table.name}</Link>
                    </td>
                    <td>
                        {table.number_of_rows}
                    </td>
                    <td>
                        {table.number_of_columns}
                    </td>
                    <td>
                        {Math.round(table.average_percentage_of_nulls * 100)}%
                    </td>
                    <td>
                        <input 
                            type="checkbox" checked={table.use_for_bi}
                            onClick={() => {this.updateUseForBi(table)}}
                            />
                    </td>
                </tr>);
        });

        return (
            <div className="TableList">
                <input 
                    type="text" value={this.state.query}
                    onChange={this.handleSearch}
                    placeholder="Filter for tables"
                />
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Table</th>
                            <th>Number of rows</th>
                            <th>Number of columns</th>
                            <th>Avg null in columns</th>
                            <th>Use for BI</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>

                <ReactPaginate 
                    pageCount={this.state.numberOfPages}
                    pageRangeDisplayed={5}
                    marginPagesDisplayed={2}
                    onPageChange={(page) => this.pageChanged(page.selected)} />
            </div>
        );
    }
}

export default TableList;
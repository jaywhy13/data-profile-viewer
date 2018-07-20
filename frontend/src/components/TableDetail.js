import React from 'react';
import axios from 'axios';

import ColumnRow from './ColumnRow';
import './TableList.css';
import ReactPaginate from 'react-paginate';
import ReactModal from 'react-modal';


class TableDetail extends React.Component {

    state = {
        name: "...",
        columns: [],
        limit: 30,
        offset: 0,
        total: 0,
        numberOfPages: 0,
        query: "",
        showModal: false,
        columnValueDistrubtions: []
    }

    constructor() {
        super();
        this.handleSearch = this.handleSearch.bind(this);
        this.showValueDistributions = this.showValueDistributions.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }

    componentDidMount () {
        let urlParams = this.props.match.params;
        let name = urlParams.table;
        this.setState({
            name
        }, (prevState, props) => {
            this.loadColumns();
        })
    }

    pageChanged(page) {
        this.setState({
            'offset': page * 30,
        }, (prevState, props) => {
            this.loadColumns();
        })
    }


    handleSearch(event) {
        this.setState({query: event.target.value}, () => {
            this.loadColumns();
        })
    }

    showValueDistributions(columnId) {
        axios.get(`/api/column/${columnId}/value_distributions/`).then((response) => {
            this.setState({
                columnValueDistrubtions: response.data.results,
                showModal: true
            });
        });      
    }

    closeModal () {
        this.setState({
            showModal: false
        })
    }

    loadColumns() {
        // Grab the columns now
        axios.get(`/api/table/${this.state.name}/columns/?offset=${this.state.offset}&limit=${this.state.limit}&cq=${this.state.query}`).then((response) => {
            const columns = response.data.results.slice(0);
            this.setState({
                columns: columns,
                numberOfPages: Math.round(response.data.count / 30),
                total: response.data.count,
            })
        })
    }

    render() {
        let rows = this.state.columns.map((column) => {
            return (
                <ColumnRow column={column} key={column.id}
                    onColumnUniqueValueClicked={this.showValueDistributions}
                />
            );
        });

        return (

            <div>
                <h1>{this.state.name}</h1>

                <input 
                    type="text" value={this.state.query}
                    onChange={this.handleSearch}
                    placeholder="Filter for columns"
                />

                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Minimum / Maximum</th>
                            <th>Std Dev</th>
                            <th>Max Length</th>
                            <th>Null Count</th>
                            <th>Unique Values</th>
                            <th>Has Duplicates</th>
                            <th>Data Structured</th>
                            <th>Needs Index</th>
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

                <ReactModal isOpen={this.state.showModal} >
                    <div>
                        <button onClick={this.closeModal}>Close</button>
                        <table className="table table-hover">
                            <thead>
                                <tr>
                                    <th>Value</th>
                                    <th>Count</th>
                                </tr>
                            </thead>
                            <tbody>
                            {this.state.columnValueDistrubtions.map((valueDistribution) => {
                                return (
                                    <tr>
                                        <td>{valueDistribution.value}</td>
                                        <td>{valueDistribution.count}</td>
                                    </tr>
                                );
                            })}
                            </tbody>
                        </table>                        
                    </div>

                </ReactModal>

            </div>
        );
    }
};

export default TableDetail;
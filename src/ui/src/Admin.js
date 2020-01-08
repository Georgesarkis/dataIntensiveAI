import React, { Component } from "react";
import { Alert, Badge, Card } from "reactstrap";
import Form from "react-bootstrap/Form";
import Table from "react-bootstrap/Table";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.css";
import makeModelJson from "./makemodel.json";
import axios, { post, get } from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./App.css";


/**
  Admin class.

  @author @MartinStanchev
*/
class Admin extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
      fileUpload: {},
      result: "",
      error: "",
      apiUrl: "http://localhost:5000",
      toDate: new Date(),
      fromDate: new Date(),
      experiments:[]
    };
  }

  /**
    @author @MartinStanchev
  */
  onFileUploadHandler = event => {
    let file = event.target.files[0];
    this.setState({ fileUpload: event.target.files[0], error: "" });
  };

  /**
    @author @MartinStanchev
  */
  handleValidateResult = data => {
      let res = {};
      if (data.result && data.status) {
        res = {title: data.status, result: data.result, r2Img: data.R2_chart_img, maeImg: data.MAE_chart_img,  MAE: data.result[0], R2: data.result[1]};
      }
      else if (data.error) {
        res = {title: data.status, result: data.error};
      }

      this.setState({result: res});
  }

  /**
    @author @MartinStanchev @MajedDalain
  */
  handleRetrainResult = data => {
    let res = {};
    if (data.result && data.status) {
      res = { title: data.status, MAE: data.result[0], R2: data.result[1] };
    } else if (data.error) {
      res = { title: data.status, result: data.error };
    }
    
    this.setState({ result: res });
  };

  /**
    @author @MartinStanchev
  */
  handleSubmitValidate = async event => {
    const formData = new FormData();
    await formData.append("file", this.state.fileUpload);

    if (!this.state.error) {
      let result = await post(this.state.apiUrl + "/api/validate", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
      console.log(result.data);
      console.log(result.status);
      console.log(result);
      console.log("here is the result");
      this.handleValidateResult(result.data);
    }
  };

  /**
    @author @MartinStanchev
  */
  handleSubmitTrain = async event => {
    if (!this.state.fromDate || !this.state.toDate) {
      return null;
    }
    if (this.state.fromDate > this.state.toDate) {
      return null;
    }

    const from = [
      this.state.fromDate.getFullYear(),
      this.state.fromDate.getMonth() + 1,
      this.state.fromDate.getDate()
    ];
    const to = [
      this.state.toDate.getFullYear(),
      this.state.toDate.getMonth() + 1,
      this.state.toDate.getDate()
    ];
    const data = {
      startDate: from,
      endDate: to
    };

    let result = await post(this.state.apiUrl + "/api/retrain", data);
    //TODO Make a separate function for this if we need to show different data.
    this.handleRetrainResult(result.data);
  }

  /**
    @author @MartinStanchev
  */
  handleDatePickFrom = (selected, event) => {
    if (selected > this.state.fromDate) {
      this.setState({
        error: "ERROR: Please set 'From' date to be before 'To' date."
      });
      return null;
    }

    this.setState({ fromDate: selected, error: "" });
  };

  /**
    @author @MartinStanchev
  */
  handleDatePickTo = (selected, event) => {
    if (selected < this.state.fromDate) {
      this.setState({
        error: "ERROR: Please set 'To' date to be after 'From' date."
      });
      return null;
    }
    this.setState({ toDate: selected, error: "" });
  };
   /**
    @author @MartinStanchev, @MajedDalain
   */
  fetchAllExperiments = async () => {
    let result = await get(this.state.apiUrl + "/api/experiments", {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });

    this.setState({experiments:result.data.result});
    this.fillExpTable(result.data.result);
    console.log(this.state.experiments)
  };

  /**
    @author @MartinStanchev, @MajedDalain
  */

  fillExpTable = (experiments) => {
    console.log(experiments);
    const experimentsItems = experiments;
    let expList = Object.keys(experimentsItems).map(function(key){
      return (<tr>
        <td>{experimentsItems[key].name}</td>
        <td>{experimentsItems[key].R2_train}</td>
        <td>{experimentsItems[key].R2_test}</td>
        <td>{experimentsItems[key].MAE_train}</td>
        <td>{experimentsItems[key].MAE_test}</td>
      </tr>)
    });

    let resultList =
    <Table striped border responsive>
      <thead>
        <tr>
          <th>Name</th>
          <th>R2 train</th>
          <th>R2 test</th>
          <th>MAE train</th>
          <th>MAE test</th>
        </tr>
      </thead>
      <tbody>
        {expList}
      </tbody>
    </Table>
    ;

    this.setState({
      expList: resultList
    });
  }

  /**
    @author @MartinStanchev, @MajedDalain
  */
  render() {
    const isLoading = this.state.isLoading;
    const result = this.state.result;
    const error = this.state.error;

    return (
      <Container>
        <div>
          <h1 className="title">Admin page </h1>
        </div>
        <Row className="admin-content-wrapper">
          <Col className="validate-form">
            <Row className="inner-title">
              <h5>Upload CSV Dataset</h5>
            </Row>
            <Row className="file-upload-wrapper">
              <input
                className="file-upload"
                type="file"
                name="file"
                onChange={this.onFileUploadHandler}
              />
            </Row>
            <Row className="form-submit-button">
              <Button
                variant="success"
                disabled={isLoading}
                onClick={this.handleSubmitValidate}
              >
                Validate
              </Button>
            </Row>
          </Col>
          <Col className="retrain-form">
            <Row className="inner-title">
              <h5>Retrain based on date when the data was uploaded</h5>
            </Row>
            <Row className="date-picker">
              <p>From: </p>
              <DatePicker
                selected={this.state.fromDate}
                onChange={this.handleDatePickFrom}
              />
              <p>To: </p>
              <DatePicker
                selected={this.state.toDate}
                onChange={this.handleDatePickTo}
              />
            </Row>
            <Row className="form-submit-button">
              <Button
                variant="success"
                disabled={isLoading}
                onClick={this.handleSubmitTrain}
              >
                Train
              </Button>
            </Row>
          </Col>
          <Col>
              <Button variant="info" onClick={this.fetchAllExperiments}>Show all Experiments</Button>
               <div>{this.state.expList}</div>
           </Col>

          <div className="content">
            {result &&
              <>
              <Row>
                <Col className="result-container">
                  <h5 className="result-title">{result.title}</h5>
                  <h4>Metrics for the Model :</h4>
                  <Row>
                    <h3>MAE value: </h3>
                    <p className="result-text">
                      <Badge color={result.MAE <= 13000 ? "success" : "danger"}>
                        {result.MAE}
                      </Badge>
                    </p>
                  </Row>
                  <Row>
                    <h3>R Square value :</h3>
                    <p className="result-text">
                      <Badge color={result.R2 > 90 ? "success" : "danger"}>
                        {result.R2}
                      </Badge>
                    </p>
                  </Row>
                </Col>
              </Row>
              <Row>
                <Col>
                  <img src={`data:image/png;base64,${result.r2Img}`} alt="" />
                </Col>
                <Col>
                  <img src={`data:image/png;base64,${result.maeImg}`} alt="" />
                </Col>
              </Row>
              </>
            }
            {error && <div className="content error">
              {error}
            </div>}
          </div>
        </Row>
      </Container>
    );
  }
}

export default Admin;

import React, { Component } from "react";
import "./App.css";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.css";
import makeModelJson from "./makemodel.json";
import axios from "axios";

/**
*   @author @MartinStanchev, @MajdedDalain
*/
class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      apiUrl: "http://localhost:5000",
      formData: {
        carBrand: "ACURA",
        modelName: "",
        modelYear: "",
        mileage: 0,
        transmission: "Automat",
        fuelType: "Diesel"
      },
      result: "",
      isCarModelTextDisable: true
    };
  }

  /**
  *   @author @MajedDalain
  */
  getBrandList() {
    let carBrands = Object.keys(makeModelJson).map(function(key) {
      return [key, makeModelJson[key]];
    });

    let carBrandTags = [];
    for (let i = 0; i < carBrands.length; i++) {
      carBrandTags.push(
        <option key={i} value={carBrands[i]["0"]}>
          {carBrands[i]["0"]}
        </option>
      );
    }

    return carBrandTags;
  }

  /**
  *   @author @MajedDalain
  */
  getModelList(makeModelJson, carBrandName) {
    let modelList;
    console.log("inside the getModelList");
    for (let key in makeModelJson) {
      if (key.indexOf(carBrandName) !== -1) {
        modelList = makeModelJson[key];
        console.log(modelList);
      }
    }
    let modelListTags = [];
    for (let i = 0; i < modelList.length; i++) {
      modelListTags.push(
        <option key={i} value={modelList[i]}>
          {modelList[i]}
        </option>
      );
    }
    return modelListTags;
  }

  /**
  *   @author @MajedDalain
  */
  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  };

  /**
  *   @author  @MajedDalain, @MartinStanchev
  */
  handlePredictClick = async event => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    //let result = await this.apiGet("/api/predicte", formData);
    let result = {};
    try {
      result = await axios.get(this.state.apiUrl + "/api/predict", {
        params: {
          carBrand: formData.carBrand,
          fuelType: formData.fuelType,
          mileage: formData.mileage,
          modelName: formData.modelName,
          modelYear: formData.modelYear,
          transmission: formData.transmission
        }
      });
    } catch (e) {
      console.log(e);
      this.setState({
        isLoading: false
      });
    }

    this.setState({
      isLoading: false
    });

    this.handleResultData(result.data);
  };

  /**
  *   @author  @MajedDalain, @MartinStanchev
  */
  handleResultData = data => {
    let res = {};
    if (!data) {
      res = { title: "Error: No data received from backend" };
    } else {
      if (data.result === "None") {
        res = {
          title:
            "Either model does not exist, or an unexpected error happened.",
          price: ""
        };
      } else if (data.error) {
        res = {
          title: data.error,
          price: ""
        };
      } else {
        res = {
          title: data.status,
          price: data.result
        };
      }
    }

    this.setState({
      result: res
    });
  };

  /**
  *   @author  @MajedDalain
  */
  handleCancelClick = event => {
    this.setState({ result: "" });
  };

  /**
  *   @author @MajedDalain, @MartinStanchev
  */
  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;
    let modelList = this.getModelList(
      makeModelJson,
      this.state.formData.carBrand
    );
    let brandElements = this.getBrandList();

    var mileage = [];
    for (let i = 0; i <= 200000; i = +(i + 1000).toFixed(1)) {
      mileage.push(
        <option key={i} value={i}>
          {i}
        </option>
      );
    }
    var modelYear = [];
    for (let i = 1960; i < 2020; i = +(i + 1).toFixed(1)) {
      modelYear.push(
        <option key={i} value={i}>
          {i}
        </option>
      );
    }

    return (
      <Container>
        <div>
          <h1 className="title">LetUS Value YoUr Car </h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Brand</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.carBrand}
                  name="carBrand"
                  onChange={this.handleChange}
                >
                  {brandElements}
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Car Model</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.modelName}
                  name="modelName"
                  onChange={this.handleChange}
                >
                  {modelList}
                </Form.Control>
              </Form.Group>
            </Form.Row>
            <br />
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Mileage</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.mileage}
                  name="mileage"
                  onChange={this.handleChange}
                >
                  {mileage}
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Model Year</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.modelYear}
                  name="modelYear"
                  onChange={this.handleChange}
                >
                  {modelYear}
                </Form.Control>
              </Form.Group>
            </Form.Row>
            <br />
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label column sm={2}>
                  Transmission
                </Form.Label>
                <Form.Control
                  as="select"
                  value={formData.transmission}
                  name="transmission"
                  onChange={this.handleChange}
                >
                  <option>Automat</option>
                  <option>Manuell</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label column sm={4}>
                  Fuel Type
                </Form.Label>
                <Form.Control
                  as="select"
                  value={formData.fuelType}
                  name="fuelType"
                  onChange={this.handleChange}
                >
                  <option>Diesel</option>
                  <option>Bensin</option>
                  <option>Hybird</option>
                  <option>El</option>
                </Form.Control>
              </Form.Group>
            </Form.Row>

            <Row id="footerRow">
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}
                >
                  {isLoading ? "Making prediction" : "Predict"}
                </Button>
              </Col>
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}
                >
                  Reset prediction
                </Button>
              </Col>
            </Row>
          </Form>
          <div className="content">
            {result && (
              <Row>
                <Col className="result-container">
                  <h5 className="result-title">{result.title}</h5>
                  <p className="result-price">{result.price}</p>
                </Col>
              </Row>
            )}
          </div>
        </div>
      </Container>
    );
  }
}

export default App;

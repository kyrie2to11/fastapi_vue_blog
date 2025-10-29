import React from 'react';
import { Container, Jumbotron, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import { useQuery } from 'react-query';
import { fetchAbout } from '../services/api';

const AboutPage = () => {
  // Fetch about page data
  const { data: about = {}, isLoading, error } = useQuery('about', fetchAbout);

  if (isLoading) {
    return (
      <Container className="mt-5 d-flex justify-content-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading about page...</span>
        </Spinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">
          Failed to load about page. Please try again later.
        </Alert>
      </Container>
    );
  }

  return (
    <Container fluid>
      <Jumbotron className="bg-light mb-4">
        <h1>About Me</h1>
        <p>
          This personal blog is a space for sharing knowledge, experiences, and daily learnings.
        </p>
      </Jumbotron>

      <Row>
        <Col md={10} className="mx-auto">
          <Card>
            <Card.Header>Introduction</Card.Header>
            <Card.Body>
              <div 
                className="about-content" 
                dangerouslySetInnerHTML={{ __html: about.content || 'No content available.' }} 
              />
            </Card.Body>
          </Card>

          <Card className="mt-4">
            <Card.Header>Interests</Card.Header>
            <Card.Body>
              <ul className="list-group list-group-flush">
                <li className="list-group-item">Web Development (React, FastAPI, Node.js)</li>
                <li className="list-group-item">Data Science & Machine Learning</li>
                <li className="list-group-item">Open Source Contributions</li>
                <li className="list-group-item">Tech Writing & Tutorials</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AboutPage;
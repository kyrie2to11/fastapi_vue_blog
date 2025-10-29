import React from 'react';
import { Container, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import { useQuery } from 'react-query';
import { fetchTools } from '../services/api';

const ToolsPage = () => {
  const { data: tools = [], isLoading, error } = useQuery('tools', fetchTools);

  if (isLoading) {
    return (
      <Container className="mt-5 d-flex justify-content-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading tools...</span>
        </Spinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">
          Failed to load tools. Please try again later.
        </Alert>
      </Container>
    );
  }

  return (
    <Container fluid>
      <h1 className="mb-5">My Tools & Resources</h1>
      
      {tools.length === 0 ? (
        <Alert variant="info">
          No tools available yet. Check back later!
        </Alert>
      ) : (
        <Row>
          {tools.map(tool => (
            <Col md={4} key={tool.id} className="mb-4">
              <Card>
                <Card.Header>{tool.name}</Card.Header>
                <Card.Body>
                  {tool.description && <p className="card-text">{tool.description}</p>}
                  {tool.link && (
                    <a href={tool.link} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
                      Visit Tool
                    </a>
                  )}
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default ToolsPage;
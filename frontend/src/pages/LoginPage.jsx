import React from 'react';
import { Container, Card, Button, Alert, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const LoginPage = () => {
  const handleOAuthLogin = (provider) => {
    // Redirect to backend OAuth endpoint
    window.location.href = `/api/v1/auth/${provider}`;
  };

  return (
    <Container fluid>
      <Row className="justify-content-center mt-5">
        <Col md={6} lg={4}>
          <Card>
            <Card.Header className="bg-primary text-white text-center">
              <h2>Social Login</h2>
            </Card.Header>
            <Card.Body>
              <Alert variant="info" className="text-center">
                Log in with your preferred social account
              </Alert>

              <div className="d-grid gap-3">
                <Button 
                  variant="dark" 
                  size="lg"
                  className="d-flex align-items-center justify-content-center"
                  onClick={() => handleOAuthLogin('github')}
                >
                  <i className="fab fa-github me-2"></i> GitHub
                </Button>
                <Button 
                  variant="success" 
                  size="lg"
                  className="d-flex align-items-center justify-content-center"
                  onClick={() => handleOAuthLogin('wechat')}
                >
                  <i className="fab fa-weixin me-2"></i> WeChat
                </Button>
                <Button 
                  variant="primary" 
                  size="lg"
                  className="d-flex align-items-center justify-content-center"
                  onClick={() => handleOAuthLogin('qq')}
                >
                  <i className="fab fa-qq me-2"></i> QQ
                </Button>
              </div>

              <div className="mt-4 text-center">
                <p className="mb-0">
                  <Link to="/register" className="text-decoration-none">Create an account</Link>
                </p>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default LoginPage;
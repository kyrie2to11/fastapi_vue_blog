import React from 'react';
import { Container, Row, Col, Card, Alert, Spinner, Button } from 'react-bootstrap';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { fetchArticleBySlug } from '../services/api';
import DateFormatter from '../utils/DateFormatter';

const BlogDetailPage = () => {
  const { slug } = useParams();

  const { data: article, isLoading, error } = useQuery(
    ['article', slug],
    () => fetchArticleBySlug(slug),
    {
      enabled: !!slug,
    }
  );

  if (isLoading) {
    return (
      <Container className="mt-5 d-flex justify-content-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading article...</span>
        </Spinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">
          Failed to load the requested article. It may have been removed or not found.
        </Alert>
        <Button as={Link} to="/blog" variant="primary">
          Back to Blog List
        </Button>
      </Container>
    );
  }

  return (
    <Container fluid>
      <div className="mb-4">
        <Link to="/blog" className="text-decoration-none">
          <Button variant="light" size="sm" className="mb-3">
            ← Back to Blog
          </Button>
        </Link>
      </div>

      {article && (
        <Row>
          <Col md={8}>
            <h1 className="mb-4">{article.title}</h1>
            <div className="text-muted mb-4">
              <span>By {article.author?.username}</span>
              <span className="mx-2">•</span>
              <span>{DateFormatter.format(article.created_at)}</span>
              {article.updated_at && (
                <>
                  <span className="mx-2">•</span>
                  <span>Updated: {DateFormatter.format(article.updated_at)}</span>
                </>
              )}
            </div>

            <Card className="mb-5">
              <Card.Body>
                <div
                  className="blog-content"
                  dangerouslySetInnerHTML={{ __html: article.content }}
                />
              </Card.Body>
            </Card>
          </Col>

          <Col md={4}>
            <Card className="mb-4">
              <Card.Header>About the Author</Card.Header>
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <div className="me-3">
                    <div className="rounded-circle bg-primary text-white w-12 h-12 d-flex align-items-center justify-content-center">
                      {article.author?.username.charAt(0).toUpperCase()}
                    </div>
                  </div>
                  <div>
                    <h5 className="mb-0">{article.author?.username}</h5>
                    <p className="text-muted mb-0">
                      {article.author?.bio || 'No bio available'}
                    </p>
                  </div>
                </div>
              </Card.Body>
            </Card>

            <Card>
              <Card.Header>Related Articles</Card.Header>
              <Card.Body>
                <ul className="list-group list-group-flush">
                  {article.related_articles?.slice(0, 3).map(relArticle => (
                    <li key={relArticle.id} className="list-group-item">
                      <Link
                        to={`/blog/${relArticle.slug}`}
                        className="text-decoration-none"
                      >
                        {relArticle.title}
                      </Link>
                    </li>
                  ))}
                </ul>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </Container>
  );
};

export default BlogDetailPage;
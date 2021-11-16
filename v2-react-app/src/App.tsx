
import React, {useCallback, useEffect, useState} from 'react';
import axios from 'axios';
import {
  Box,
  Container,
  Divider,
  Button,
  FormHelperText,
  TextField,
  Rating,
} from '@mui/material';
import { makeStyles } from '@mui/styles';
import { Formik } from 'formik';
import * as Yup from 'yup';
import set = Reflect.set;

const useStyles = makeStyles({
  root: {
  },
  container: {
  },
  courseTitle: {
    fontSize: "45px",
    fontWeight: 300,
    marginBottom: 0
  },
  reviewDescriptionText: {
    marginTop: 0
  }
});

function App() {
  const classes = useStyles();
  const [reviews, setReviews] = useState<[]>([]);
  const [newRating, setNewRating] = useState(0);
  const [product, setProduct] = useState(null);

  const getReviews = useCallback(async () => {
    const response = await axios.get(process.env.REACT_APP_SERVER_URL + `/V2/reviews`);
    console.log("RD" + response.data);
    if (response.data === null) {
    } else {
      setReviews(response.data)
    }
  }, [axios]);

  const getProduct = useCallback(async () => {
    const response = await axios.get(process.env.REACT_APP_SERVER_URL + `/V2/product`);
    console.log("RD" + response.data);
    if (response.data === null) {
    } else {
      setProduct(response.data)
    }
  }, [axios]);

  const createReview = useCallback(async (newRating, description, product) => {
    let data = {
      rating: newRating,
      description: description,
      product_id: product['id'],
    }
    let config = {
      headers: {
      }
    }
    const response = await axios.post(process.env.REACT_APP_SERVER_URL + `/V2/create-review`, data, config);
    if (response.data === null) {
    } else {
      setReviews(response.data)
      setNewRating(0)
    }
  }, [axios]);


  useEffect(() => {
    getReviews();
    getProduct();
  }, [getReviews, getProduct]);


  if (reviews === [] || product === null) {
    return null
  }

  return (
    <div className="App">
      <Container maxWidth="md" className={classes.container}>
        <Box>
          <h1 className={classes.courseTitle}> My Awesome Course</h1>
          <Box
              mb={2}
              display={'flex'}
              alignItems={'center'}
          >
            <Rating name="read-only" value={product['average']} precision={0.5} readOnly />
            <Box ml={1}><p><strong>({product['average']})</strong></p></Box>
          </Box>
        </Box>
        <Divider />
        <Box mb={2} mt={2}>
          <h2>Submit a review:</h2>
          <Rating
              name="simple-controlled"
              size={'large'}
              value={newRating}
              precision={0.5}
              onChange={(event, newValue) => {
                if (newValue !== null) {
                  setNewRating(newValue);
                }
              }}
          />
          <Box pr={{xs:0, sm:0, md:50}}>
            <Formik
                initialValues={{
                  description: '',
                  submit: null
                }}
                validationSchema={Yup.object().shape({
                  description: Yup.string().max(250),
                })}
                onSubmit={async (values, {
                  resetForm
                }) => {
                  try {
                    await createReview(newRating, values.description, product);
                    resetForm();
                  } catch (err) {
                    console.error(err);
                  }
                }}
            >
              {({
                  errors,
                  handleBlur,
                  handleChange,
                  handleSubmit,
                  isSubmitting,
                  touched,
                  values,
                }) => (
                  <form
                      noValidate
                      onSubmit={handleSubmit}
                  >

                    <TextField
                        error={Boolean(touched.description && errors.description)}
                        fullWidth
                        helperText={touched.description && errors.description}
                        label="Optional text..."
                        margin="normal"
                        name="description"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        type="description"
                        value={values.description}
                        variant="outlined"
                        multiline
                        rows={3}
                        maxRows={10}
                    />
                    {errors.submit && (
                        <Box mt={3}>
                          <FormHelperText error>
                            {errors.submit}
                          </FormHelperText>
                        </Box>
                    )}
                    <Box mt={2}>
                      <Button
                          disabled={isSubmitting}
                          size="large"
                          type="submit"
                          variant="contained"
                      >
                        Submit review
                      </Button>
                    </Box>
                  </form>
              )}
            </Formik>
          </Box>

        </Box>
        <Divider />
        <Box>
          <>
            {reviews.map((review) => (
                <>
                  <Box
                      mb={0}
                      mt={2}
                      display={'flex'}
                      alignItems={'center'}
                  >
                    <Rating name="read-only" value={review['rating']} precision={0.5} readOnly />
                    <Box ml={1}><p><strong>({review['rating']})</strong></p></Box>
                  </Box>
                  <Box mb={2}><p className={classes.reviewDescriptionText}>{review['description']}</p></Box>
                </>
              ))}
          </>
        </Box>
      </Container>
    </div>
  );
}

export default App;
